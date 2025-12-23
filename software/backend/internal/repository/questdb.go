// internal/repository/questdb.go
// QuestDB client for LUXX HAUS time-series data
//
// IMPORTANT: QuestDB's PostgreSQL wire protocol does NOT support parameterized queries.
// All parameters must be safely escaped and interpolated into query strings.
// This implementation uses strict input validation and secure escaping to prevent SQL injection.
package repository

import (
	"context"
	"database/sql"
	"fmt"
	"regexp"
	"strconv"
	"strings"
	"time"

	_ "github.com/lib/pq" // QuestDB uses PostgreSQL wire protocol
	"github.com/luxx-haus/api/internal/models"
)

// QuestDB wraps the database connection
type QuestDB struct {
	db *sql.DB
}

// Validation patterns for secure parameter handling
var (
	// alphanumericPattern matches only safe alphanumeric identifiers with hyphens/underscores
	alphanumericPattern = regexp.MustCompile(`^[a-zA-Z0-9_-]+$`)
	// apiKeyPattern matches expected API key format
	apiKeyPattern = regexp.MustCompile(`^[a-zA-Z0-9_-]{16,128}$`)
	// symbolPattern matches QuestDB SYMBOL values (alphanumeric with common chars)
	symbolPattern = regexp.MustCompile(`^[a-zA-Z0-9_-]{1,64}$`)
)

// escapeString safely escapes a string for QuestDB SQL queries
// This prevents SQL injection by escaping single quotes
func escapeString(s string) string {
	return strings.ReplaceAll(s, "'", "''")
}

// validateIdentifier ensures an identifier is safe for use in queries
func validateIdentifier(id string) error {
	if !alphanumericPattern.MatchString(id) {
		return fmt.Errorf("invalid identifier format: %s", id)
	}
	return nil
}

// validateAPIKey ensures API key format is valid
func validateAPIKey(key string) error {
	if !apiKeyPattern.MatchString(key) {
		return fmt.Errorf("invalid API key format")
	}
	return nil
}

// NewQuestDB creates a new QuestDB connection
func NewQuestDB(host string, port int, user, pass string) (*QuestDB, error) {
	connStr := fmt.Sprintf(
		"host=%s port=%d user=%s password=%s dbname=qdb sslmode=disable",
		host, port, user, pass,
	)

	db, err := sql.Open("postgres", connStr)
	if err != nil {
		return nil, fmt.Errorf("failed to open connection: %w", err)
	}

	// Configure connection pool for high-throughput time-series workload
	db.SetMaxOpenConns(50)
	db.SetMaxIdleConns(25)
	db.SetConnMaxLifetime(5 * time.Minute)

	// Verify connection
	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel()

	if err := db.PingContext(ctx); err != nil {
		return nil, fmt.Errorf("failed to ping database: %w", err)
	}

	return &QuestDB{db: db}, nil
}

// Close closes the database connection
func (q *QuestDB) Close() error {
	return q.db.Close()
}

// Ping checks database connectivity
func (q *QuestDB) Ping(ctx context.Context) error {
	return q.db.PingContext(ctx)
}

// ============================================
// CARRIER OPERATIONS
// ============================================

// GetCarrierByAPIKey retrieves carrier by API key
func (q *QuestDB) GetCarrierByAPIKey(ctx context.Context, apiKey string) (*models.Carrier, error) {
	if err := validateAPIKey(apiKey); err != nil {
		return nil, err
	}

	query := fmt.Sprintf(`
		SELECT carrier_id, name, api_key, tier, home_limit, webhook_url, active, created_at, updated_at
		FROM carriers
		WHERE api_key = '%s' AND active = true
		LATEST ON created_at PARTITION BY carrier_id
	`, escapeString(apiKey))

	carrier := &models.Carrier{}
	err := q.db.QueryRowContext(ctx, query).Scan(
		&carrier.CarrierID, &carrier.Name, &carrier.APIKey, &carrier.Tier,
		&carrier.HomeLimit, &carrier.WebhookURL, &carrier.Active,
		&carrier.CreatedAt, &carrier.UpdatedAt,
	)
	if err != nil {
		return nil, err
	}

	return carrier, nil
}

// ============================================
// HOME OPERATIONS
// ============================================

// GetHomeByPolicy retrieves home by policy number
func (q *QuestDB) GetHomeByPolicy(ctx context.Context, carrierID, policyNumber string) (*models.Home, error) {
	if err := validateIdentifier(carrierID); err != nil {
		return nil, err
	}

	query := fmt.Sprintf(`
		SELECT home_id, carrier_id, policy_number, address, city, state, zip,
			   latitude, longitude, square_feet, year_built, health_score,
			   risk_tier, tesla_site_id, installed_at, last_reading, active
		FROM homes
		WHERE carrier_id = '%s' AND policy_number = '%s' AND active = true
		LATEST ON installed_at PARTITION BY home_id
	`, escapeString(carrierID), escapeString(policyNumber))

	home := &models.Home{}
	err := q.db.QueryRowContext(ctx, query).Scan(
		&home.HomeID, &home.CarrierID, &home.PolicyNumber, &home.Address,
		&home.City, &home.State, &home.Zip, &home.Latitude, &home.Longitude,
		&home.SquareFeet, &home.YearBuilt, &home.HealthScore, &home.RiskTier,
		&home.TeslaSiteID, &home.InstalledAt, &home.LastReading, &home.Active,
	)
	if err != nil {
		return nil, err
	}

	return home, nil
}

// GetHomeByID retrieves home by ID
func (q *QuestDB) GetHomeByID(ctx context.Context, homeID string) (*models.Home, error) {
	if err := validateIdentifier(homeID); err != nil {
		return nil, err
	}

	query := fmt.Sprintf(`
		SELECT home_id, carrier_id, policy_number, address, city, state, zip,
			   latitude, longitude, square_feet, year_built, health_score,
			   risk_tier, tesla_site_id, installed_at, last_reading, active
		FROM homes
		WHERE home_id = '%s' AND active = true
		LATEST ON installed_at PARTITION BY home_id
	`, escapeString(homeID))

	home := &models.Home{}
	err := q.db.QueryRowContext(ctx, query).Scan(
		&home.HomeID, &home.CarrierID, &home.PolicyNumber, &home.Address,
		&home.City, &home.State, &home.Zip, &home.Latitude, &home.Longitude,
		&home.SquareFeet, &home.YearBuilt, &home.HealthScore, &home.RiskTier,
		&home.TeslaSiteID, &home.InstalledAt, &home.LastReading, &home.Active,
	)
	if err != nil {
		return nil, err
	}

	return home, nil
}

// GetHomesByCarrier retrieves all homes for a carrier
func (q *QuestDB) GetHomesByCarrier(ctx context.Context, carrierID string) ([]models.Home, error) {
	if err := validateIdentifier(carrierID); err != nil {
		return nil, err
	}

	query := fmt.Sprintf(`
		SELECT home_id, carrier_id, policy_number, address, city, state, zip,
			   latitude, longitude, square_feet, year_built, health_score,
			   risk_tier, tesla_site_id, installed_at, last_reading, active
		FROM homes
		WHERE carrier_id = '%s' AND active = true
		LATEST ON installed_at PARTITION BY home_id
	`, escapeString(carrierID))

	rows, err := q.db.QueryContext(ctx, query)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	var homes []models.Home
	for rows.Next() {
		var home models.Home
		err := rows.Scan(
			&home.HomeID, &home.CarrierID, &home.PolicyNumber, &home.Address,
			&home.City, &home.State, &home.Zip, &home.Latitude, &home.Longitude,
			&home.SquareFeet, &home.YearBuilt, &home.HealthScore, &home.RiskTier,
			&home.TeslaSiteID, &home.InstalledAt, &home.LastReading, &home.Active,
		)
		if err != nil {
			return nil, err
		}
		homes = append(homes, home)
	}

	return homes, nil
}

// ============================================
// SENSOR READINGS
// ============================================

// GetSensorReadings retrieves readings with filters
func (q *QuestDB) GetSensorReadings(ctx context.Context, filters models.ReadingFilters) ([]models.SensorReading, error) {
	if err := validateIdentifier(filters.HomeID); err != nil {
		return nil, err
	}

	query := fmt.Sprintf(`
		SELECT ts, sensor_id, home_id, sensor_type,
			   flow_rate, pressure, temperature, moisture_detected,
			   methane_ppm, co_ppm, gas_alarm,
			   tilt_x, tilt_y, crack_displacement, vibration_magnitude,
			   supply_temp, return_temp, filter_pressure_drop, current_draw, efficiency_score,
			   co2_ppm, pm25, pm10, voc_index, humidity, air_temp,
			   solar_power, grid_power, battery_power, battery_soc, home_power,
			   anomaly_score, anomaly_type
		FROM sensor_readings
		WHERE home_id = '%s'
	`, escapeString(filters.HomeID))

	if filters.SensorType != "" {
		if err := validateIdentifier(filters.SensorType); err != nil {
			return nil, err
		}
		query += fmt.Sprintf(" AND sensor_type = '%s'", escapeString(filters.SensorType))
	}

	if filters.SensorID != "" {
		if err := validateIdentifier(filters.SensorID); err != nil {
			return nil, err
		}
		query += fmt.Sprintf(" AND sensor_id = '%s'", escapeString(filters.SensorID))
	}

	if !filters.StartTime.IsZero() {
		query += fmt.Sprintf(" AND ts >= '%s'", filters.StartTime.UTC().Format(time.RFC3339Nano))
	}

	if !filters.EndTime.IsZero() {
		query += fmt.Sprintf(" AND ts <= '%s'", filters.EndTime.UTC().Format(time.RFC3339Nano))
	}

	limit := filters.Limit
	if limit == 0 || limit > 10000 {
		limit = 1000
	}
	query += fmt.Sprintf(" ORDER BY ts DESC LIMIT %d", limit)

	rows, err := q.db.QueryContext(ctx, query)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	var readings []models.SensorReading
	for rows.Next() {
		var r models.SensorReading
		var flowRate, pressure, temperature sql.NullFloat64
		var moistureDetected sql.NullBool
		var methanePPM, coPPM sql.NullFloat64
		var gasAlarm sql.NullBool
		var tiltX, tiltY, crackDisplacement, vibrationMagnitude sql.NullFloat64
		var supplyTemp, returnTemp, filterPressureDrop, currentDraw, efficiencyScore sql.NullFloat64
		var co2PPM, pm25, pm10, vocIndex, humidity, airTemp sql.NullFloat64
		var solarPower, gridPower, batteryPower, batterySOC, homePower sql.NullFloat64
		var anomalyScore sql.NullFloat64
		var anomalyType sql.NullString

		err := rows.Scan(
			&r.Timestamp, &r.SensorID, &r.HomeID, &r.SensorType,
			&flowRate, &pressure, &temperature, &moistureDetected,
			&methanePPM, &coPPM, &gasAlarm,
			&tiltX, &tiltY, &crackDisplacement, &vibrationMagnitude,
			&supplyTemp, &returnTemp, &filterPressureDrop, &currentDraw, &efficiencyScore,
			&co2PPM, &pm25, &pm10, &vocIndex, &humidity, &airTemp,
			&solarPower, &gridPower, &batteryPower, &batterySOC, &homePower,
			&anomalyScore, &anomalyType,
		)
		if err != nil {
			return nil, err
		}

		// Build values map based on sensor type
		r.Values = make(map[string]interface{})
		switch r.SensorType {
		case "water":
			if flowRate.Valid {
				r.Values["flow_rate"] = flowRate.Float64
			}
			if pressure.Valid {
				r.Values["pressure"] = pressure.Float64
			}
			if temperature.Valid {
				r.Values["temperature"] = temperature.Float64
			}
			if moistureDetected.Valid {
				r.Values["moisture_detected"] = moistureDetected.Bool
			}
		case "gas":
			if methanePPM.Valid {
				r.Values["methane_ppm"] = methanePPM.Float64
			}
			if coPPM.Valid {
				r.Values["co_ppm"] = coPPM.Float64
			}
			if gasAlarm.Valid {
				r.Values["gas_alarm"] = gasAlarm.Bool
			}
		case "structural":
			if tiltX.Valid {
				r.Values["tilt_x"] = tiltX.Float64
			}
			if tiltY.Valid {
				r.Values["tilt_y"] = tiltY.Float64
			}
			if crackDisplacement.Valid {
				r.Values["crack_displacement"] = crackDisplacement.Float64
			}
			if vibrationMagnitude.Valid {
				r.Values["vibration_magnitude"] = vibrationMagnitude.Float64
			}
		case "hvac":
			if supplyTemp.Valid {
				r.Values["supply_temp"] = supplyTemp.Float64
			}
			if returnTemp.Valid {
				r.Values["return_temp"] = returnTemp.Float64
			}
			if filterPressureDrop.Valid {
				r.Values["filter_pressure_drop"] = filterPressureDrop.Float64
			}
			if currentDraw.Valid {
				r.Values["current_draw"] = currentDraw.Float64
			}
			if efficiencyScore.Valid {
				r.Values["efficiency_score"] = efficiencyScore.Float64
			}
		case "air":
			if co2PPM.Valid {
				r.Values["co2_ppm"] = co2PPM.Float64
			}
			if pm25.Valid {
				r.Values["pm25"] = pm25.Float64
			}
			if pm10.Valid {
				r.Values["pm10"] = pm10.Float64
			}
			if vocIndex.Valid {
				r.Values["voc_index"] = vocIndex.Float64
			}
			if humidity.Valid {
				r.Values["humidity"] = humidity.Float64
			}
			if airTemp.Valid {
				r.Values["air_temp"] = airTemp.Float64
			}
		case "energy":
			if solarPower.Valid {
				r.Values["solar_power"] = solarPower.Float64
			}
			if gridPower.Valid {
				r.Values["grid_power"] = gridPower.Float64
			}
			if batteryPower.Valid {
				r.Values["battery_power"] = batteryPower.Float64
			}
			if batterySOC.Valid {
				r.Values["battery_soc"] = batterySOC.Float64
			}
			if homePower.Valid {
				r.Values["home_power"] = homePower.Float64
			}
		}

		// Add anomaly info if present
		if anomalyScore.Valid && anomalyScore.Float64 > 0.5 {
			r.Anomaly = &models.AnomalyInfo{
				Score: anomalyScore.Float64,
				Type:  anomalyType.String,
			}
		}

		readings = append(readings, r)
	}

	return readings, nil
}

// GetRecentReadings retrieves readings from last N duration
func (q *QuestDB) GetRecentReadings(ctx context.Context, homeID string, duration time.Duration) ([]models.SensorReading, error) {
	filters := models.ReadingFilters{
		HomeID:    homeID,
		StartTime: time.Now().Add(-duration),
		Limit:     10000,
	}
	return q.GetSensorReadings(ctx, filters)
}

// ============================================
// RISK SCORES
// ============================================

// GetLatestRiskScores retrieves most recent scores for a home
func (q *QuestDB) GetLatestRiskScores(ctx context.Context, homeID string) (*models.RiskScores, error) {
	if err := validateIdentifier(homeID); err != nil {
		return nil, err
	}

	query := fmt.Sprintf(`
		SELECT ts, home_id, water_score, gas_score, structural_score,
			   hvac_score, air_score, energy_score, fire_score,
			   overall_score, risk_tier, confidence, model_version
		FROM risk_scores
		WHERE home_id = '%s'
		LATEST ON ts PARTITION BY home_id
	`, escapeString(homeID))

	scores := &models.RiskScores{}
	err := q.db.QueryRowContext(ctx, query).Scan(
		&scores.Timestamp, &scores.HomeID, &scores.WaterScore,
		&scores.GasScore, &scores.StructuralScore, &scores.HVACScore,
		&scores.AirScore, &scores.EnergyScore, &scores.FireScore,
		&scores.OverallScore, &scores.RiskTier, &scores.Confidence,
		&scores.ModelVersion,
	)
	if err != nil {
		return nil, err
	}

	return scores, nil
}

// InsertRiskScore stores a new risk score
func (q *QuestDB) InsertRiskScore(ctx context.Context, scores *models.RiskScores) error {
	if err := validateIdentifier(scores.HomeID); err != nil {
		return err
	}

	query := fmt.Sprintf(`
		INSERT INTO risk_scores (
			ts, home_id, water_score, gas_score, structural_score,
			hvac_score, air_score, energy_score, fire_score,
			overall_score, risk_tier, confidence, model_version
		) VALUES ('%s', '%s', %f, %f, %f, %f, %f, %f, %f, %f, '%s', %f, '%s')
	`,
		scores.Timestamp.UTC().Format(time.RFC3339Nano),
		escapeString(scores.HomeID),
		scores.WaterScore, scores.GasScore, scores.StructuralScore,
		scores.HVACScore, scores.AirScore, scores.EnergyScore, scores.FireScore,
		scores.OverallScore,
		escapeString(scores.RiskTier),
		scores.Confidence,
		escapeString(scores.ModelVersion),
	)

	_, err := q.db.ExecContext(ctx, query)
	return err
}

// ============================================
// EVENTS
// ============================================

// GetRecentEvents retrieves recent events for a home
func (q *QuestDB) GetRecentEvents(ctx context.Context, homeID string, days int) ([]models.Event, error) {
	if err := validateIdentifier(homeID); err != nil {
		return nil, err
	}

	// Sanitize days parameter
	if days <= 0 || days > 365 {
		days = 30
	}

	query := fmt.Sprintf(`
		SELECT event_id, ts, home_id, sensor_id, event_type, severity,
			   description, sensor_value, threshold_value, automated_action,
			   action_taken_at, resolved, resolved_at, resolution_notes,
			   claim_prevented, estimated_savings
		FROM events
		WHERE home_id = '%s' AND ts >= dateadd('d', -%d, now())
		ORDER BY ts DESC
		LIMIT 100
	`, escapeString(homeID), days)

	rows, err := q.db.QueryContext(ctx, query)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	var events []models.Event
	for rows.Next() {
		var e models.Event
		var actionTakenAt, resolvedAt sql.NullTime

		err := rows.Scan(
			&e.EventID, &e.Timestamp, &e.HomeID, &e.SensorID, &e.EventType,
			&e.Severity, &e.Description, &e.SensorValue, &e.ThresholdValue,
			&e.AutomatedAction, &actionTakenAt, &e.Resolved, &resolvedAt,
			&e.ResolutionNotes, &e.ClaimPrevented, &e.EstimatedSavings,
		)
		if err != nil {
			return nil, err
		}

		if actionTakenAt.Valid {
			e.ActionTakenAt = &actionTakenAt.Time
		}
		if resolvedAt.Valid {
			e.ResolvedAt = &resolvedAt.Time
		}

		events = append(events, e)
	}

	return events, nil
}

// GetActivePredictions retrieves active predictions for a home
func (q *QuestDB) GetActivePredictions(ctx context.Context, homeID string) ([]models.Prediction, error) {
	if err := validateIdentifier(homeID); err != nil {
		return nil, err
	}

	query := fmt.Sprintf(`
		SELECT ts, home_id, prediction_type, probability, days_to_event,
			   severity, recommended_action, confidence, model_version
		FROM predictions
		WHERE home_id = '%s' AND ts >= dateadd('d', -7, now())
		ORDER BY probability DESC
		LIMIT 10
	`, escapeString(homeID))

	rows, err := q.db.QueryContext(ctx, query)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	var predictions []models.Prediction
	for rows.Next() {
		var p models.Prediction
		err := rows.Scan(
			&p.Timestamp, &p.HomeID, &p.PredictionType, &p.Probability,
			&p.DaysToEvent, &p.Severity, &p.RecommendedAction,
			&p.Confidence, &p.ModelVersion,
		)
		if err != nil {
			return nil, err
		}
		predictions = append(predictions, p)
	}

	return predictions, nil
}

// GetClaimStats retrieves claim prevention statistics
func (q *QuestDB) GetClaimStats(ctx context.Context, homeID string, year int) (*models.ClaimStats, error) {
	if err := validateIdentifier(homeID); err != nil {
		return nil, err
	}

	// Sanitize year parameter
	currentYear := time.Now().Year()
	if year < 2020 || year > currentYear+1 {
		year = currentYear
	}

	startOfYear := time.Date(year, 1, 1, 0, 0, 0, 0, time.UTC)
	endOfYear := time.Date(year+1, 1, 1, 0, 0, 0, 0, time.UTC)

	query := fmt.Sprintf(`
		SELECT count() as prevented_count, sum(estimated_savings) as total_savings
		FROM events
		WHERE home_id = '%s'
		  AND claim_prevented = true
		  AND ts >= '%s'
		  AND ts < '%s'
	`, escapeString(homeID), startOfYear.Format(time.RFC3339), endOfYear.Format(time.RFC3339))

	stats := &models.ClaimStats{Year: year}
	var totalSavings sql.NullFloat64

	err := q.db.QueryRowContext(ctx, query).Scan(
		&stats.PreventedCount, &totalSavings,
	)
	if err != nil {
		return nil, err
	}

	if totalSavings.Valid {
		stats.EstimatedSavings = totalSavings.Float64
	}

	return stats, nil
}

// ============================================
// PORTFOLIO ANALYTICS
// ============================================

// GetPortfolioStats retrieves aggregate statistics for a carrier
func (q *QuestDB) GetPortfolioStats(ctx context.Context, carrierID string) (*models.PortfolioRiskResponse, error) {
	if err := validateIdentifier(carrierID); err != nil {
		return nil, err
	}

	query := fmt.Sprintf(`
		SELECT
			count() as total,
			sum(CASE WHEN risk_tier = 'low' THEN 1 ELSE 0 END) as low_risk,
			sum(CASE WHEN risk_tier = 'medium' THEN 1 ELSE 0 END) as medium_risk,
			sum(CASE WHEN risk_tier = 'high' THEN 1 ELSE 0 END) as high_risk,
			sum(CASE WHEN risk_tier = 'critical' THEN 1 ELSE 0 END) as critical_risk,
			avg(health_score) as avg_score
		FROM homes
		WHERE carrier_id = '%s' AND active = true
		LATEST ON installed_at PARTITION BY home_id
	`, escapeString(carrierID))

	response := &models.PortfolioRiskResponse{
		CarrierID:   carrierID,
		LastUpdated: time.Now(),
	}

	err := q.db.QueryRowContext(ctx, query).Scan(
		&response.TotalHomes,
		&response.RiskDistribution.Low,
		&response.RiskDistribution.Medium,
		&response.RiskDistribution.High,
		&response.RiskDistribution.Critical,
		&response.AverageScore,
	)
	if err != nil {
		return nil, err
	}

	response.ActiveHomes = response.TotalHomes

	return response, nil
}

// GetHighRiskHomes retrieves homes with critical or high risk
func (q *QuestDB) GetHighRiskHomes(ctx context.Context, carrierID string, limit int) ([]models.HighRiskHome, error) {
	if err := validateIdentifier(carrierID); err != nil {
		return nil, err
	}

	// Sanitize limit
	if limit <= 0 || limit > 100 {
		limit = 10
	}

	query := fmt.Sprintf(`
		SELECT home_id, policy_number, health_score, risk_tier
		FROM homes
		WHERE carrier_id = '%s' AND active = true AND risk_tier IN ('high', 'critical')
		LATEST ON installed_at PARTITION BY home_id
		ORDER BY health_score ASC
		LIMIT %d
	`, escapeString(carrierID), limit)

	rows, err := q.db.QueryContext(ctx, query)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	var homes []models.HighRiskHome
	for rows.Next() {
		var h models.HighRiskHome
		err := rows.Scan(&h.HomeID, &h.PolicyNumber, &h.HealthScore, &h.PrimaryRisk)
		if err != nil {
			return nil, err
		}
		homes = append(homes, h)
	}

	return homes, nil
}

// GetSensorsByHome retrieves all sensors for a home
func (q *QuestDB) GetSensorsByHome(ctx context.Context, homeID string) ([]models.Sensor, error) {
	if err := validateIdentifier(homeID); err != nil {
		return nil, err
	}

	query := fmt.Sprintf(`
		SELECT sensor_id, home_id, sensor_type, model, location,
			   firmware_version, battery_level, signal_strength, protocol,
			   installed_at, last_seen, active
		FROM sensors
		WHERE home_id = '%s' AND active = true
		LATEST ON installed_at PARTITION BY sensor_id
	`, escapeString(homeID))

	rows, err := q.db.QueryContext(ctx, query)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	var sensors []models.Sensor
	for rows.Next() {
		var s models.Sensor
		err := rows.Scan(
			&s.SensorID, &s.HomeID, &s.SensorType, &s.Model, &s.Location,
			&s.FirmwareVersion, &s.BatteryLevel, &s.SignalStrength, &s.Protocol,
			&s.InstalledAt, &s.LastSeen, &s.Active,
		)
		if err != nil {
			return nil, err
		}
		sensors = append(sensors, s)
	}

	return sensors, nil
}

// Ensure strconv is used (for future numeric conversions)
var _ = strconv.Itoa
