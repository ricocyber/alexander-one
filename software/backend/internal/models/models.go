// internal/models/models.go
// Data models for LUXX HAUS API
package models

import (
	"database/sql"
	"time"
)

// ============================================
// CORE ENTITIES
// ============================================

// Carrier represents an insurance carrier partner
type Carrier struct {
	CarrierID  string    `json:"carrier_id" db:"carrier_id"`
	Name       string    `json:"name" db:"name"`
	APIKey     string    `json:"-" db:"api_key"` // Never expose
	Tier       string    `json:"tier" db:"tier"` // starter, growth, enterprise
	HomeLimit  int       `json:"home_limit" db:"home_limit"`
	WebhookURL string    `json:"webhook_url" db:"webhook_url"`
	Active     bool      `json:"active" db:"active"`
	CreatedAt  time.Time `json:"created_at" db:"created_at"`
	UpdatedAt  time.Time `json:"updated_at" db:"updated_at"`
}

// Home represents a monitored property
type Home struct {
	HomeID       string         `json:"home_id" db:"home_id"`
	CarrierID    string         `json:"carrier_id" db:"carrier_id"`
	PolicyNumber string         `json:"policy_number" db:"policy_number"`
	Address      string         `json:"address" db:"address"`
	City         string         `json:"city" db:"city"`
	State        string         `json:"state" db:"state"`
	Zip          string         `json:"zip" db:"zip"`
	Latitude     float64        `json:"latitude" db:"latitude"`
	Longitude    float64        `json:"longitude" db:"longitude"`
	SquareFeet   int            `json:"square_feet" db:"square_feet"`
	YearBuilt    int            `json:"year_built" db:"year_built"`
	HealthScore  float64        `json:"health_score" db:"health_score"`
	RiskTier     string         `json:"risk_tier" db:"risk_tier"`
	TeslaSiteID  sql.NullString `json:"tesla_site_id" db:"tesla_site_id"`
	InstalledAt  time.Time      `json:"installed_at" db:"installed_at"`
	LastReading  time.Time      `json:"last_reading" db:"last_reading"`
	Active       bool           `json:"active" db:"active"`
}

// Sensor represents an individual monitoring device
type Sensor struct {
	SensorID        string    `json:"sensor_id" db:"sensor_id"`
	HomeID          string    `json:"home_id" db:"home_id"`
	SensorType      string    `json:"sensor_type" db:"sensor_type"` // water, gas, structural, hvac, air, valve, fire, irrigation
	Model           string    `json:"model" db:"model"`
	Location        string    `json:"location" db:"location"`
	FirmwareVersion string    `json:"firmware_version" db:"firmware_version"`
	BatteryLevel    float64   `json:"battery_level" db:"battery_level"`
	SignalStrength  int       `json:"signal_strength" db:"signal_strength"`
	Protocol        string    `json:"protocol" db:"protocol"` // matter, zigbee, zwave, wifi
	InstalledAt     time.Time `json:"installed_at" db:"installed_at"`
	LastSeen        time.Time `json:"last_seen" db:"last_seen"`
	Active          bool      `json:"active" db:"active"`
}

// ============================================
// SENSOR READINGS
// ============================================

// SensorReading represents a single data point
type SensorReading struct {
	Timestamp  time.Time              `json:"timestamp" db:"ts"`
	SensorID   string                 `json:"sensor_id" db:"sensor_id"`
	HomeID     string                 `json:"home_id" db:"home_id"`
	SensorType string                 `json:"sensor_type" db:"sensor_type"`
	Location   string                 `json:"location,omitempty"`
	Values     map[string]interface{} `json:"values"`
	Anomaly    *AnomalyInfo           `json:"anomaly,omitempty"`
}

// AnomalyInfo contains anomaly detection results
type AnomalyInfo struct {
	Score       float64 `json:"score"`
	Type        string  `json:"type"`
	Description string  `json:"description"`
}

// WaterReading for AquaGuard sensors
type WaterReading struct {
	FlowRate         float64 `json:"flow_rate" db:"flow_rate"`                   // L/min
	Pressure         float64 `json:"pressure" db:"pressure"`                     // PSI
	Temperature      float64 `json:"temperature" db:"temperature"`               // Celsius
	MoistureDetected bool    `json:"moisture_detected" db:"moisture_detected"`
}

// GasReading for FlameShield sensors
type GasReading struct {
	MethanePPM float64 `json:"methane_ppm" db:"methane_ppm"`
	COPPM      float64 `json:"co_ppm" db:"co_ppm"`
	GasAlarm   bool    `json:"gas_alarm" db:"gas_alarm"`
}

// StructuralReading for FoundationWatch sensors
type StructuralReading struct {
	TiltX              float64 `json:"tilt_x" db:"tilt_x"`                           // degrees
	TiltY              float64 `json:"tilt_y" db:"tilt_y"`
	CrackDisplacement  float64 `json:"crack_displacement" db:"crack_displacement"`   // mm
	VibrationMagnitude float64 `json:"vibration_magnitude" db:"vibration_magnitude"`
}

// HVACReading for ClimateCore sensors
type HVACReading struct {
	SupplyTemp         float64 `json:"supply_temp" db:"supply_temp"`
	ReturnTemp         float64 `json:"return_temp" db:"return_temp"`
	FilterPressureDrop float64 `json:"filter_pressure_drop" db:"filter_pressure_drop"`
	CurrentDraw        float64 `json:"current_draw" db:"current_draw"` // Amps
	EfficiencyScore    float64 `json:"efficiency_score" db:"efficiency_score"`
}

// AirReading for AirPure sensors
type AirReading struct {
	CO2PPM   float64 `json:"co2_ppm" db:"co2_ppm"`
	PM25     float64 `json:"pm25" db:"pm25"`       // µg/m³
	PM10     float64 `json:"pm10" db:"pm10"`
	VOCIndex float64 `json:"voc_index" db:"voc_index"`
	Humidity float64 `json:"humidity" db:"humidity"` // %
	AirTemp  float64 `json:"air_temp" db:"air_temp"`
}

// EnergyReading for Tesla integration
type EnergyReading struct {
	SolarPower   float64 `json:"solar_power" db:"solar_power"`     // Watts
	GridPower    float64 `json:"grid_power" db:"grid_power"`
	BatteryPower float64 `json:"battery_power" db:"battery_power"`
	BatterySOC   float64 `json:"battery_soc" db:"battery_soc"` // State of charge %
	HomePower    float64 `json:"home_power" db:"home_power"`
}

// ============================================
// RISK SCORES
// ============================================

// RiskScores contains all category risk scores for a home
type RiskScores struct {
	Timestamp       time.Time `json:"timestamp" db:"ts"`
	HomeID          string    `json:"home_id" db:"home_id"`
	WaterScore      float64   `json:"water_score" db:"water_score"`
	GasScore        float64   `json:"gas_score" db:"gas_score"`
	StructuralScore float64   `json:"structural_score" db:"structural_score"`
	HVACScore       float64   `json:"hvac_score" db:"hvac_score"`
	AirScore        float64   `json:"air_score" db:"air_score"`
	EnergyScore     float64   `json:"energy_score" db:"energy_score"`
	FireScore       float64   `json:"fire_score" db:"fire_score"`
	OverallScore    float64   `json:"overall_score" db:"overall_score"`
	RiskTier        string    `json:"risk_tier" db:"risk_tier"`
	Confidence      float64   `json:"confidence" db:"confidence"`
	ModelVersion    string    `json:"model_version" db:"model_version"`
}

// ============================================
// EVENTS
// ============================================

// Event represents a detected incident
type Event struct {
	EventID         string     `json:"event_id" db:"event_id"`
	Timestamp       time.Time  `json:"timestamp" db:"ts"`
	HomeID          string     `json:"home_id" db:"home_id"`
	SensorID        string     `json:"sensor_id" db:"sensor_id"`
	EventType       string     `json:"event_type" db:"event_type"` // leak_detected, gas_alert, freeze_warning, etc.
	Severity        string     `json:"severity" db:"severity"`     // info, warning, critical
	Description     string     `json:"description" db:"description"`
	SensorValue     float64    `json:"sensor_value" db:"sensor_value"`
	ThresholdValue  float64    `json:"threshold_value" db:"threshold_value"`
	AutomatedAction string     `json:"automated_action,omitempty" db:"automated_action"`
	ActionTakenAt   *time.Time `json:"action_taken_at,omitempty" db:"action_taken_at"`
	Resolved        bool       `json:"resolved" db:"resolved"`
	ResolvedAt      *time.Time `json:"resolved_at,omitempty" db:"resolved_at"`
	ResolutionNotes string     `json:"resolution_notes,omitempty" db:"resolution_notes"`
	ClaimPrevented  bool       `json:"claim_prevented" db:"claim_prevented"`
	EstimatedSavings float64   `json:"estimated_savings" db:"estimated_savings"`
}

// Prediction from ML models
type Prediction struct {
	Timestamp         time.Time `json:"timestamp" db:"ts"`
	HomeID            string    `json:"home_id" db:"home_id"`
	PredictionType    string    `json:"type" db:"prediction_type"` // water_leak, hvac_failure, freeze_risk, etc.
	Probability       float64   `json:"probability" db:"probability"`
	DaysToEvent       int       `json:"days_to_event,omitempty" db:"days_to_event"`
	Severity          string    `json:"severity" db:"severity"`
	RecommendedAction string    `json:"recommended_action" db:"recommended_action"`
	Confidence        float64   `json:"confidence" db:"confidence"`
	ModelVersion      string    `json:"model_version" db:"model_version"`
}

// ============================================
// API RESPONSES
// ============================================

// HomeHealthResponse is the primary API response
type HomeHealthResponse struct {
	HomeID           string           `json:"home_id"`
	PolicyNumber     string           `json:"policy_number"`
	Address          string           `json:"address"`
	HealthScore      float64          `json:"health_score"`
	RiskTier         string           `json:"risk_tier"`
	LastReading      time.Time        `json:"last_reading"`
	RiskBreakdown    RiskBreakdown    `json:"risk_breakdown"`
	Predictions      []Prediction     `json:"predictions"`
	RecentEvents     []Event          `json:"recent_events"`
	ClaimsPrevented  int              `json:"claims_prevented_ytd"`
	EstimatedSavings float64          `json:"estimated_savings_ytd"`
	TeslaIntegration *TeslaStatus     `json:"tesla_integration,omitempty"`
}

// RiskBreakdown contains category scores
type RiskBreakdown struct {
	Water      CategoryScore `json:"water"`
	Gas        CategoryScore `json:"gas"`
	Structural CategoryScore `json:"structural"`
	HVAC       CategoryScore `json:"hvac"`
	Air        CategoryScore `json:"air"`
	Energy     CategoryScore `json:"energy"`
	Fire       CategoryScore `json:"fire"`
}

// CategoryScore for a single risk category
type CategoryScore struct {
	Score   float64      `json:"score"`
	Trend   string       `json:"trend"` // improving, stable, declining
	Factors []RiskFactor `json:"factors"`
}

// RiskFactor contributing to risk
type RiskFactor struct {
	Name        string  `json:"name"`
	Value       float64 `json:"value"`
	Threshold   float64 `json:"threshold"`
	Impact      string  `json:"impact"` // positive, neutral, negative
	Description string  `json:"description"`
}

// TeslaStatus for Powerwall integration
type TeslaStatus struct {
	Connected     bool      `json:"connected"`
	SiteID        string    `json:"site_id"`
	SolarPower    float64   `json:"solar_power_w"`
	BatteryPower  float64   `json:"battery_power_w"`
	BatterySOC    float64   `json:"battery_soc_percent"`
	GridPower     float64   `json:"grid_power_w"`
	HomePower     float64   `json:"home_power_w"`
	GridStatus    string    `json:"grid_status"`
	StormWatch    bool      `json:"storm_watch_active"`
	BackupReserve float64   `json:"backup_reserve_percent"`
	LastUpdated   time.Time `json:"last_updated"`
}

// PortfolioRiskResponse for carrier-level view
type PortfolioRiskResponse struct {
	CarrierID        string           `json:"carrier_id"`
	TotalHomes       int              `json:"total_homes"`
	ActiveHomes      int              `json:"active_homes"`
	RiskDistribution RiskDistribution `json:"risk_distribution"`
	AverageScore     float64          `json:"average_health_score"`
	TrendDirection   string           `json:"trend_direction"`
	HighRiskHomes    []HighRiskHome   `json:"high_risk_homes"`
	RecentAlerts     int              `json:"alerts_last_24h"`
	ClaimsPrevented  int              `json:"claims_prevented_ytd"`
	EstimatedSavings float64          `json:"estimated_savings_ytd"`
	LastUpdated      time.Time        `json:"last_updated"`
}

// RiskDistribution by tier
type RiskDistribution struct {
	Low      int `json:"low"`
	Medium   int `json:"medium"`
	High     int `json:"high"`
	Critical int `json:"critical"`
}

// HighRiskHome summary
type HighRiskHome struct {
	HomeID       string  `json:"home_id"`
	PolicyNumber string  `json:"policy_number"`
	HealthScore  float64 `json:"health_score"`
	PrimaryRisk  string  `json:"primary_risk"`
	DaysAtRisk   int     `json:"days_at_risk"`
}

// ============================================
// WEBHOOKS
// ============================================

// WebhookSubscription configuration
type WebhookSubscription struct {
	SubscriptionID string    `json:"subscription_id"`
	CarrierID      string    `json:"carrier_id"`
	URL            string    `json:"url"`
	Events         []string  `json:"events"` // leak_detected, gas_alert, critical_risk
	Secret         string    `json:"-"`      // For HMAC verification
	Active         bool      `json:"active"`
	CreatedAt      time.Time `json:"created_at"`
}

// WebhookPayload for outbound webhooks
type WebhookPayload struct {
	EventType    string      `json:"event_type"`
	Timestamp    time.Time   `json:"timestamp"`
	HomeID       string      `json:"home_id"`
	PolicyNumber string      `json:"policy_number"`
	Severity     string      `json:"severity"`
	Data         interface{} `json:"data"`
	Signature    string      `json:"signature"`
}

// ============================================
// CLAIMS
// ============================================

// ClaimDocumentation for insurance claims
type ClaimDocumentation struct {
	ClaimID           string          `json:"claim_id"`
	EventID           string          `json:"event_id"`
	HomeID            string          `json:"home_id"`
	PolicyNumber      string          `json:"policy_number"`
	Timestamp         time.Time       `json:"timestamp"`
	EventType         string          `json:"event_type"`
	Timeline          []TimelineEntry `json:"timeline"`
	ReadingsBefore    []SensorReading `json:"readings_before"`
	ReadingsDuring    []SensorReading `json:"readings_during"`
	ReadingsAfter     []SensorReading `json:"readings_after"`
	AutomatedResponse string          `json:"automated_response"`
	Outcome           string          `json:"outcome"` // prevented, mitigated, claim_filed
	EstimatedDamage   float64         `json:"estimated_damage_prevented"`
}

// TimelineEntry for claim documentation
type TimelineEntry struct {
	Timestamp   time.Time `json:"timestamp"`
	Event       string    `json:"event"`
	Description string    `json:"description"`
	Source      string    `json:"source"` // sensor, system, user
}

// ============================================
// QUERY FILTERS
// ============================================

// ReadingFilters for querying sensor data
type ReadingFilters struct {
	HomeID     string
	SensorID   string
	SensorType string
	StartTime  time.Time
	EndTime    time.Time
	Limit      int
}

// ClaimStats for a home
type ClaimStats struct {
	PreventedCount   int     `json:"prevented_count"`
	EstimatedSavings float64 `json:"estimated_savings"`
	Year             int     `json:"year"`
}
