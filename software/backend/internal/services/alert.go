// internal/services/alert.go
// Alert service for LUXX HAUS notifications
package services

import (
	"context"
	"crypto/hmac"
	"crypto/sha256"
	"encoding/hex"
	"encoding/json"
	"fmt"
	"net/http"
	"strings"
	"time"

	"github.com/luxx-haus/api/internal/models"
	"github.com/luxx-haus/api/internal/repository"
)

// AlertService handles alerts and notifications
type AlertService struct {
	db    *repository.QuestDB
	cache *repository.Redis
}

// NewAlertService creates a new AlertService
func NewAlertService(db *repository.QuestDB, cache *repository.Redis) *AlertService {
	return &AlertService{db: db, cache: cache}
}

// AlertThresholds define trigger points
var AlertThresholds = map[string]map[string]float64{
	"water": {
		"leak_critical":     0.9,
		"leak_warning":      0.7,
		"pressure_low":      30.0,
		"pressure_high":     80.0,
		"moisture_detected": 1.0,
	},
	"gas": {
		"methane_warning":  1000.0, // ppm
		"methane_critical": 5000.0,
		"co_warning":       35.0,
		"co_critical":      100.0,
	},
	"structural": {
		"tilt_warning":  0.5,  // degrees
		"tilt_critical": 1.0,
		"crack_warning": 2.0,  // mm
		"crack_critical": 5.0,
	},
	"hvac": {
		"efficiency_warning": 70.0,
		"filter_clogged":     1.5,
	},
	"air": {
		"co2_warning":   1000.0,
		"co2_critical":  2000.0,
		"pm25_warning":  35.0,
		"pm25_critical": 150.0,
	},
}

// ProcessReading evaluates a reading and generates alerts if needed
func (s *AlertService) ProcessReading(ctx context.Context, reading *models.SensorReading) (*models.Event, error) {
	var event *models.Event

	switch reading.SensorType {
	case "water":
		event = s.evaluateWaterReading(reading)
	case "gas":
		event = s.evaluateGasReading(reading)
	case "structural":
		event = s.evaluateStructuralReading(reading)
	case "hvac":
		event = s.evaluateHVACReading(reading)
	case "air":
		event = s.evaluateAirReading(reading)
	}

	if event != nil {
		// Check if we should deduplicate (avoid alert storms)
		dedupeKey := fmt.Sprintf("alert:%s:%s:%s", reading.HomeID, reading.SensorType, event.EventType)
		exists, _ := s.cache.Exists(ctx, dedupeKey)
		if exists {
			return nil, nil // Skip duplicate
		}

		// Set dedupe key with 5 minute TTL
		s.cache.Set(ctx, dedupeKey, "1", 5*time.Minute)

		// Determine automated action
		event.AutomatedAction = s.determineAction(event)

		// Send webhook notifications
		go s.sendWebhooks(context.Background(), event)
	}

	return event, nil
}

func (s *AlertService) evaluateWaterReading(r *models.SensorReading) *models.Event {
	// Check anomaly score from ML
	if r.Anomaly != nil && r.Anomaly.Score >= AlertThresholds["water"]["leak_critical"] {
		return &models.Event{
			Timestamp:   r.Timestamp,
			HomeID:      r.HomeID,
			SensorID:    r.SensorID,
			EventType:   "leak_detected",
			Severity:    "critical",
			Description: "Critical water leak detected by ML model",
			SensorValue: r.Anomaly.Score,
		}
	}

	if r.Anomaly != nil && r.Anomaly.Score >= AlertThresholds["water"]["leak_warning"] {
		return &models.Event{
			Timestamp:   r.Timestamp,
			HomeID:      r.HomeID,
			SensorID:    r.SensorID,
			EventType:   "leak_warning",
			Severity:    "warning",
			Description: "Potential water leak detected",
			SensorValue: r.Anomaly.Score,
		}
	}

	// Check moisture sensor
	if moisture, ok := r.Values["moisture_detected"].(bool); ok && moisture {
		return &models.Event{
			Timestamp:   r.Timestamp,
			HomeID:      r.HomeID,
			SensorID:    r.SensorID,
			EventType:   "moisture_alert",
			Severity:    "warning",
			Description: "Moisture detected in monitored area",
		}
	}

	// Check pressure
	if pressure, ok := r.Values["pressure"].(float64); ok {
		if pressure < AlertThresholds["water"]["pressure_low"] {
			return &models.Event{
				Timestamp:      r.Timestamp,
				HomeID:         r.HomeID,
				SensorID:       r.SensorID,
				EventType:      "low_pressure",
				Severity:       "warning",
				Description:    "Water pressure below normal range",
				SensorValue:    pressure,
				ThresholdValue: AlertThresholds["water"]["pressure_low"],
			}
		}
	}

	return nil
}

func (s *AlertService) evaluateGasReading(r *models.SensorReading) *models.Event {
	// CRITICAL PATH - gas alerts are life safety
	
	if methane, ok := r.Values["methane_ppm"].(float64); ok {
		if methane >= AlertThresholds["gas"]["methane_critical"] {
			return &models.Event{
				Timestamp:      r.Timestamp,
				HomeID:         r.HomeID,
				SensorID:       r.SensorID,
				EventType:      "gas_leak_critical",
				Severity:       "critical",
				Description:    "CRITICAL: Dangerous methane levels detected - evacuate immediately",
				SensorValue:    methane,
				ThresholdValue: AlertThresholds["gas"]["methane_critical"],
			}
		}
		if methane >= AlertThresholds["gas"]["methane_warning"] {
			return &models.Event{
				Timestamp:      r.Timestamp,
				HomeID:         r.HomeID,
				SensorID:       r.SensorID,
				EventType:      "gas_leak_warning",
				Severity:       "warning",
				Description:    "Elevated methane levels detected",
				SensorValue:    methane,
				ThresholdValue: AlertThresholds["gas"]["methane_warning"],
			}
		}
	}

	if co, ok := r.Values["co_ppm"].(float64); ok {
		if co >= AlertThresholds["gas"]["co_critical"] {
			return &models.Event{
				Timestamp:      r.Timestamp,
				HomeID:         r.HomeID,
				SensorID:       r.SensorID,
				EventType:      "co_critical",
				Severity:       "critical",
				Description:    "CRITICAL: Dangerous carbon monoxide levels - evacuate immediately",
				SensorValue:    co,
				ThresholdValue: AlertThresholds["gas"]["co_critical"],
			}
		}
		if co >= AlertThresholds["gas"]["co_warning"] {
			return &models.Event{
				Timestamp:      r.Timestamp,
				HomeID:         r.HomeID,
				SensorID:       r.SensorID,
				EventType:      "co_warning",
				Severity:       "warning",
				Description:    "Elevated carbon monoxide levels detected",
				SensorValue:    co,
				ThresholdValue: AlertThresholds["gas"]["co_warning"],
			}
		}
	}

	return nil
}

func (s *AlertService) evaluateStructuralReading(r *models.SensorReading) *models.Event {
	if crack, ok := r.Values["crack_displacement"].(float64); ok {
		if crack >= AlertThresholds["structural"]["crack_critical"] {
			return &models.Event{
				Timestamp:      r.Timestamp,
				HomeID:         r.HomeID,
				SensorID:       r.SensorID,
				EventType:      "structural_critical",
				Severity:       "critical",
				Description:    "Critical foundation movement detected",
				SensorValue:    crack,
				ThresholdValue: AlertThresholds["structural"]["crack_critical"],
			}
		}
	}

	return nil
}

func (s *AlertService) evaluateHVACReading(r *models.SensorReading) *models.Event {
	if eff, ok := r.Values["efficiency_score"].(float64); ok {
		if eff < AlertThresholds["hvac"]["efficiency_warning"] {
			return &models.Event{
				Timestamp:      r.Timestamp,
				HomeID:         r.HomeID,
				SensorID:       r.SensorID,
				EventType:      "hvac_efficiency_low",
				Severity:       "warning",
				Description:    "HVAC efficiency below optimal range",
				SensorValue:    eff,
				ThresholdValue: AlertThresholds["hvac"]["efficiency_warning"],
			}
		}
	}

	if filter, ok := r.Values["filter_pressure_drop"].(float64); ok {
		if filter >= AlertThresholds["hvac"]["filter_clogged"] {
			return &models.Event{
				Timestamp:   r.Timestamp,
				HomeID:      r.HomeID,
				SensorID:    r.SensorID,
				EventType:   "filter_clogged",
				Severity:    "info",
				Description: "HVAC filter needs replacement",
			}
		}
	}

	return nil
}

func (s *AlertService) evaluateAirReading(r *models.SensorReading) *models.Event {
	if pm25, ok := r.Values["pm25"].(float64); ok {
		if pm25 >= AlertThresholds["air"]["pm25_critical"] {
			return &models.Event{
				Timestamp:   r.Timestamp,
				HomeID:      r.HomeID,
				SensorID:    r.SensorID,
				EventType:   "air_quality_critical",
				Severity:    "critical",
				Description: "Hazardous air quality - take immediate action",
				SensorValue: pm25,
			}
		}
	}

	return nil
}

// determineAction decides what automated action to take
func (s *AlertService) determineAction(event *models.Event) string {
	switch event.EventType {
	case "leak_detected", "leak_warning":
		return "valve_closed"
	case "gas_leak_critical":
		return "gas_shutoff_activated"
	case "freeze_warning":
		return "hvac_heat_mode"
	default:
		return "alert_sent"
	}
}

// sendWebhooks sends event notifications to carrier webhooks
func (s *AlertService) sendWebhooks(ctx context.Context, event *models.Event) {
	// Get home to find carrier
	home, err := s.db.GetHomeByID(ctx, event.HomeID)
	if err != nil {
		return
	}

	// Get carrier webhook URL (would query subscriptions)
	carrier, err := s.db.GetCarrierByAPIKey(ctx, home.CarrierID)
	if err != nil || carrier.WebhookURL == "" {
		return
	}

	// Build payload
	payload := models.WebhookPayload{
		EventType:    event.EventType,
		Timestamp:    event.Timestamp,
		HomeID:       event.HomeID,
		PolicyNumber: home.PolicyNumber,
		Severity:     event.Severity,
		Data:         event,
	}

	// Sign payload
	payloadBytes, _ := json.Marshal(payload)
	signature := signPayload(payloadBytes, "webhook_secret") // Would use actual secret
	payload.Signature = signature

	// Send webhook
	s.sendHTTPWebhook(carrier.WebhookURL, payload)
}

func (s *AlertService) sendHTTPWebhook(url string, payload models.WebhookPayload) error {
	payloadBytes, err := json.Marshal(payload)
	if err != nil {
		return err
	}

	req, err := http.NewRequest("POST", url, strings.NewReader(string(payloadBytes)))
	if err != nil {
		return err
	}

	req.Header.Set("Content-Type", "application/json")
	req.Header.Set("X-LUXX-Signature", payload.Signature)
	req.Header.Set("X-LUXX-Timestamp", payload.Timestamp.Format(time.RFC3339))

	client := &http.Client{Timeout: 10 * time.Second}
	resp, err := client.Do(req)
	if err != nil {
		return err
	}
	defer resp.Body.Close()

	return nil
}

func signPayload(payload []byte, secret string) string {
	h := hmac.New(sha256.New, []byte(secret))
	h.Write(payload)
	return hex.EncodeToString(h.Sum(nil))
}
