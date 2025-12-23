// internal/config/config.go
// Configuration management for LUXX HAUS API
package config

import (
	"os"
	"strconv"
)

// Config holds all configuration values
type Config struct {
	// Server
	Port        string
	Environment string

	// QuestDB
	QuestDBHost string
	QuestDBPort int
	QuestDBUser string
	QuestDBPass string

	// Redis
	RedisHost string
	RedisPort int
	RedisPass string

	// MQTT
	MQTTBroker   string
	MQTTPort     int
	MQTTUser     string
	MQTTPass     string
	MQTTClientID string

	// Tesla Fleet API
	TeslaClientID     string
	TeslaClientSecret string
	TeslaPrivateKey   string

	// Rate Limiting
	RateLimitRPS int

	// ML Models
	ONNXModelPath string

	// Security
	JWTSecret string
}

// Load reads configuration from environment variables
func Load() *Config {
	return &Config{
		// Server
		Port:        getEnv("PORT", "8080"),
		Environment: getEnv("ENVIRONMENT", "development"),

		// QuestDB
		QuestDBHost: getEnv("QUESTDB_HOST", "localhost"),
		QuestDBPort: getEnvInt("QUESTDB_PORT", 8812),
		QuestDBUser: getEnv("QUESTDB_USER", "admin"),
		QuestDBPass: getEnv("QUESTDB_PASS", "quest"),

		// Redis
		RedisHost: getEnv("REDIS_HOST", "localhost"),
		RedisPort: getEnvInt("REDIS_PORT", 6379),
		RedisPass: getEnv("REDIS_PASS", ""),

		// MQTT
		MQTTBroker:   getEnv("MQTT_BROKER", "localhost"),
		MQTTPort:     getEnvInt("MQTT_PORT", 1883),
		MQTTUser:     getEnv("MQTT_USER", ""),
		MQTTPass:     getEnv("MQTT_PASS", ""),
		MQTTClientID: getEnv("MQTT_CLIENT_ID", "luxx-api"),

		// Tesla
		TeslaClientID:     getEnv("TESLA_CLIENT_ID", ""),
		TeslaClientSecret: getEnv("TESLA_CLIENT_SECRET", ""),
		TeslaPrivateKey:   getEnv("TESLA_PRIVATE_KEY_PATH", "/etc/luxx/tesla.pem"),

		// Rate Limiting
		RateLimitRPS: getEnvInt("RATE_LIMIT_RPS", 100),

		// ML Models
		ONNXModelPath: getEnv("ONNX_MODEL_PATH", "/opt/luxx/models"),

		// Security
		JWTSecret: getEnv("JWT_SECRET", "change-me-in-production"),
	}
}

func getEnv(key, defaultValue string) string {
	if value := os.Getenv(key); value != "" {
		return value
	}
	return defaultValue
}

func getEnvInt(key string, defaultValue int) int {
	if value := os.Getenv(key); value != "" {
		if intVal, err := strconv.Atoi(value); err == nil {
			return intVal
		}
	}
	return defaultValue
}
