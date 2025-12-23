// pkg/mqtt/client.go
// MQTT client for LUXX HAUS sensor communication
package mqtt

import (
	"crypto/tls"
	"crypto/x509"
	"encoding/json"
	"fmt"
	"log"
	"os"
	"sync"
	"time"

	mqtt "github.com/eclipse/paho.mqtt.golang"
)

// Client wraps the MQTT client
type Client struct {
	client    mqtt.Client
	connected bool
	mu        sync.RWMutex
	handlers  map[string]MessageHandler
}

// MessageHandler processes incoming MQTT messages
type MessageHandler func(topic string, payload []byte)

// Config for MQTT connection
type Config struct {
	Broker      string
	Port        int
	ClientID    string
	Username    string
	Password    string
	CACertPath  string
	ClientCert  string
	ClientKey   string
	UseTLS      bool
}

// SensorReading is the standard message format from sensors
type SensorReading struct {
	SensorID   string                 `json:"sensor_id"`
	HomeID     string                 `json:"home_id"`
	SensorType string                 `json:"sensor_type"`
	Timestamp  time.Time              `json:"timestamp"`
	Values     map[string]interface{} `json:"values"`
}

// Command is a message sent to sensors
type Command struct {
	CommandID string                 `json:"command_id"`
	Command   string                 `json:"command"`
	Params    map[string]interface{} `json:"params,omitempty"`
	Timestamp time.Time              `json:"timestamp"`
}

// Alert is a critical notification
type Alert struct {
	AlertID    string    `json:"alert_id"`
	HomeID     string    `json:"home_id"`
	SensorID   string    `json:"sensor_id"`
	AlertType  string    `json:"alert_type"`
	Severity   string    `json:"severity"`
	Message    string    `json:"message"`
	Timestamp  time.Time `json:"timestamp"`
}

// NewClient creates a new MQTT client
func NewClient(cfg *Config) (*Client, error) {
	opts := mqtt.NewClientOptions()

	// Build broker URL
	protocol := "tcp"
	if cfg.UseTLS {
		protocol = "ssl"
	}
	brokerURL := fmt.Sprintf("%s://%s:%d", protocol, cfg.Broker, cfg.Port)
	opts.AddBroker(brokerURL)

	opts.SetClientID(cfg.ClientID)
	opts.SetUsername(cfg.Username)
	opts.SetPassword(cfg.Password)

	// Connection settings
	opts.SetKeepAlive(60 * time.Second)
	opts.SetPingTimeout(10 * time.Second)
	opts.SetAutoReconnect(true)
	opts.SetMaxReconnectInterval(30 * time.Second)
	opts.SetConnectRetry(true)
	opts.SetConnectRetryInterval(5 * time.Second)
	opts.SetCleanSession(false) // Persistent session

	// TLS configuration
	if cfg.UseTLS {
		tlsConfig, err := createTLSConfig(cfg)
		if err != nil {
			return nil, fmt.Errorf("failed to create TLS config: %w", err)
		}
		opts.SetTLSConfig(tlsConfig)
	}

	client := &Client{
		handlers: make(map[string]MessageHandler),
	}

	// Connection handlers
	opts.SetOnConnectHandler(func(c mqtt.Client) {
		client.mu.Lock()
		client.connected = true
		client.mu.Unlock()
		log.Println("✅ MQTT connected")
		
		// Resubscribe on reconnect
		client.resubscribe()
	})

	opts.SetConnectionLostHandler(func(c mqtt.Client, err error) {
		client.mu.Lock()
		client.connected = false
		client.mu.Unlock()
		log.Printf("❌ MQTT connection lost: %v", err)
	})

	opts.SetReconnectingHandler(func(c mqtt.Client, opts *mqtt.ClientOptions) {
		log.Println("🔄 MQTT reconnecting...")
	})

	client.client = mqtt.NewClient(opts)

	// Connect
	if token := client.client.Connect(); token.Wait() && token.Error() != nil {
		return nil, fmt.Errorf("failed to connect: %w", token.Error())
	}

	return client, nil
}

// createTLSConfig builds TLS configuration with mTLS support
func createTLSConfig(cfg *Config) (*tls.Config, error) {
	tlsConfig := &tls.Config{
		MinVersion: tls.VersionTLS12,
	}

	// Load CA certificate
	if cfg.CACertPath != "" {
		caCert, err := os.ReadFile(cfg.CACertPath)
		if err != nil {
			return nil, fmt.Errorf("failed to read CA cert: %w", err)
		}
		caCertPool := x509.NewCertPool()
		caCertPool.AppendCertsFromPEM(caCert)
		tlsConfig.RootCAs = caCertPool
	}

	// Load client certificate for mTLS
	if cfg.ClientCert != "" && cfg.ClientKey != "" {
		cert, err := tls.LoadX509KeyPair(cfg.ClientCert, cfg.ClientKey)
		if err != nil {
			return nil, fmt.Errorf("failed to load client cert: %w", err)
		}
		tlsConfig.Certificates = []tls.Certificate{cert}
	}

	return tlsConfig, nil
}

// Close disconnects the client
func (c *Client) Close() {
	c.client.Disconnect(1000)
}

// IsConnected returns connection status
func (c *Client) IsConnected() bool {
	c.mu.RLock()
	defer c.mu.RUnlock()
	return c.connected
}

// Subscribe adds a subscription with a handler
func (c *Client) Subscribe(topic string, qos byte, handler MessageHandler) error {
	c.mu.Lock()
	c.handlers[topic] = handler
	c.mu.Unlock()

	token := c.client.Subscribe(topic, qos, func(client mqtt.Client, msg mqtt.Message) {
		handler(msg.Topic(), msg.Payload())
	})

	if token.Wait() && token.Error() != nil {
		return token.Error()
	}

	log.Printf("📥 Subscribed to: %s", topic)
	return nil
}

// Unsubscribe removes a subscription
func (c *Client) Unsubscribe(topic string) error {
	c.mu.Lock()
	delete(c.handlers, topic)
	c.mu.Unlock()

	token := c.client.Unsubscribe(topic)
	if token.Wait() && token.Error() != nil {
		return token.Error()
	}

	return nil
}

// resubscribe restores subscriptions after reconnect
func (c *Client) resubscribe() {
	c.mu.RLock()
	handlers := make(map[string]MessageHandler)
	for topic, handler := range c.handlers {
		handlers[topic] = handler
	}
	c.mu.RUnlock()

	for topic, handler := range handlers {
		if err := c.Subscribe(topic, 1, handler); err != nil {
			log.Printf("Failed to resubscribe to %s: %v", topic, err)
		}
	}
}

// PublishReading sends a sensor reading (QoS 1)
func (c *Client) PublishReading(homeID, sensorID string, reading *SensorReading) error {
	topic := fmt.Sprintf("luxx/%s/sensors/%s/readings", homeID, sensorID)
	return c.publishJSON(topic, 1, false, reading)
}

// PublishAlert sends an alert (QoS 1, Retained for critical)
func (c *Client) PublishAlert(homeID string, alert *Alert) error {
	topic := fmt.Sprintf("luxx/%s/alerts/%s", homeID, alert.Severity)
	retained := alert.Severity == "critical"
	return c.publishJSON(topic, 1, retained, alert)
}

// PublishCommand sends a command to a sensor (QoS 2 for guaranteed delivery)
func (c *Client) PublishCommand(homeID, deviceType, deviceID string, command *Command) error {
	topic := fmt.Sprintf("luxx/%s/commands/%s/%s", homeID, deviceType, deviceID)
	return c.publishJSON(topic, 2, false, command)
}

// PublishStatus publishes hub/sensor status
func (c *Client) PublishStatus(homeID, deviceID string, status map[string]interface{}) error {
	topic := fmt.Sprintf("luxx/%s/sensors/%s/status", homeID, deviceID)
	return c.publishJSON(topic, 0, true, status)
}

// publishJSON marshals and publishes a message
func (c *Client) publishJSON(topic string, qos byte, retained bool, payload interface{}) error {
	data, err := json.Marshal(payload)
	if err != nil {
		return fmt.Errorf("failed to marshal payload: %w", err)
	}

	token := c.client.Publish(topic, qos, retained, data)
	if token.Wait() && token.Error() != nil {
		return token.Error()
	}

	return nil
}

// SubscribeToHomeReadings subscribes to all sensor readings for a home
func (c *Client) SubscribeToHomeReadings(homeID string, handler func(*SensorReading)) error {
	topic := fmt.Sprintf("luxx/%s/sensors/+/readings", homeID)
	
	return c.Subscribe(topic, 1, func(t string, payload []byte) {
		var reading SensorReading
		if err := json.Unmarshal(payload, &reading); err != nil {
			log.Printf("Failed to parse reading: %v", err)
			return
		}
		handler(&reading)
	})
}

// SubscribeToHomeAlerts subscribes to all alerts for a home
func (c *Client) SubscribeToHomeAlerts(homeID string, handler func(*Alert)) error {
	topic := fmt.Sprintf("luxx/%s/alerts/+", homeID)
	
	return c.Subscribe(topic, 1, func(t string, payload []byte) {
		var alert Alert
		if err := json.Unmarshal(payload, &alert); err != nil {
			log.Printf("Failed to parse alert: %v", err)
			return
		}
		handler(&alert)
	})
}

// SubscribeToCommands subscribes to commands for a device
func (c *Client) SubscribeToCommands(homeID, deviceType, deviceID string, handler func(*Command)) error {
	topic := fmt.Sprintf("luxx/%s/commands/%s/%s", homeID, deviceType, deviceID)
	
	return c.Subscribe(topic, 2, func(t string, payload []byte) {
		var cmd Command
		if err := json.Unmarshal(payload, &cmd); err != nil {
			log.Printf("Failed to parse command: %v", err)
			return
		}
		handler(&cmd)
	})
}
