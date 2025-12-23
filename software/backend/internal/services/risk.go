// internal/services/risk.go
// Risk scoring service for LUXX HAUS
package services

import (
	"context"
	"math"
	"time"

	"github.com/luxx-haus/api/internal/models"
	"github.com/luxx-haus/api/internal/repository"
)

// RiskService calculates risk scores for homes
type RiskService struct {
	db *repository.QuestDB
}

// NewRiskService creates a new RiskService
func NewRiskService(db *repository.QuestDB) *RiskService {
	return &RiskService{db: db}
}

// Category weights for overall score (safety-critical weighted higher)
var categoryWeights = map[string]float64{
	"gas":        0.25, // Highest - life safety
	"water":      0.20, // High - major damage potential
	"structural": 0.15, // Medium-high
	"hvac":       0.10,
	"air":        0.10,
	"energy":     0.10,
	"fire":       0.10,
}

// CalculateHomeRisk computes comprehensive risk scores for a home
func (s *RiskService) CalculateHomeRisk(ctx context.Context, homeID string) (*models.RiskScores, error) {
	// Get recent readings (24 hours)
	readings, err := s.db.GetRecentReadings(ctx, homeID, 24*time.Hour)
	if err != nil {
		return nil, err
	}

	// Get recent events (30 days)
	events, err := s.db.GetRecentEvents(ctx, homeID, 30)
	if err != nil {
		return nil, err
	}

	// Calculate individual category scores
	scores := &models.RiskScores{
		Timestamp:    time.Now().UTC(),
		HomeID:       homeID,
		ModelVersion: "2.0.0",
	}

	// Group readings by sensor type
	readingsByType := groupReadingsByType(readings)

	// Calculate each category score
	scores.WaterScore = s.calculateWaterScore(readingsByType["water"], events)
	scores.GasScore = s.calculateGasScore(readingsByType["gas"], events)
	scores.StructuralScore = s.calculateStructuralScore(readingsByType["structural"], events)
	scores.HVACScore = s.calculateHVACScore(readingsByType["hvac"], events)
	scores.AirScore = s.calculateAirScore(readingsByType["air"], events)
	scores.EnergyScore = s.calculateEnergyScore(readingsByType["energy"], events)
	scores.FireScore = s.calculateFireScore(events)

	// Calculate weighted overall score
	scores.OverallScore = 
		scores.WaterScore*categoryWeights["water"] +
		scores.GasScore*categoryWeights["gas"] +
		scores.StructuralScore*categoryWeights["structural"] +
		scores.HVACScore*categoryWeights["hvac"] +
		scores.AirScore*categoryWeights["air"] +
		scores.EnergyScore*categoryWeights["energy"] +
		scores.FireScore*categoryWeights["fire"]

	// Determine risk tier
	scores.RiskTier = determineRiskTier(scores.OverallScore)

	// Calculate confidence based on data completeness
	scores.Confidence = calculateConfidence(len(readings))

	// Store the score
	if err := s.db.InsertRiskScore(ctx, scores); err != nil {
		return nil, err
	}

	return scores, nil
}

// calculateWaterScore computes water risk (100 = best)
func (s *RiskService) calculateWaterScore(readings []models.SensorReading, events []models.Event) float64 {
	score := 100.0

	// Check for recent leak events
	for _, event := range events {
		if event.EventType == "leak_detected" || event.EventType == "moisture_alert" {
			daysSince := time.Since(event.Timestamp).Hours() / 24
			if daysSince < 7 {
				score -= 30 // Recent leak is major deduction
			} else if daysSince < 30 {
				score -= 15
			}
		}
	}

	if len(readings) == 0 {
		return max(score, 50) // No data penalty
	}

	// Analyze pressure patterns
	var pressures []float64
	for _, r := range readings {
		if p, ok := r.Values["pressure"].(float64); ok {
			pressures = append(pressures, p)
		}
	}

	if len(pressures) > 0 {
		avgPressure := average(pressures)
		stdPressure := stdDev(pressures)

		// High variance indicates issues
		if stdPressure/avgPressure > 0.2 {
			score -= 10
		}

		// Abnormal pressure ranges
		if avgPressure < 30 {
			score -= 15 // Too low
		} else if avgPressure > 80 {
			score -= 10 // Too high
		}
	}

	// Check for anomalies
	for _, r := range readings {
		if r.Anomaly != nil && r.Anomaly.Score > 0.7 {
			score -= 5
		}
	}

	return max(score, 0)
}

// calculateGasScore computes gas risk (100 = best)
func (s *RiskService) calculateGasScore(readings []models.SensorReading, events []models.Event) float64 {
	score := 100.0

	// Gas events are CRITICAL
	for _, event := range events {
		if event.EventType == "gas_leak" || event.EventType == "co_alert" {
			if event.Severity == "critical" {
				score -= 50
			} else {
				daysSince := time.Since(event.Timestamp).Hours() / 24
				if daysSince < 7 {
					score -= 25
				}
			}
		}
	}

	// Check readings
	for _, r := range readings {
		if methane, ok := r.Values["methane_ppm"].(float64); ok {
			if methane > 100 {
				score -= 5 // Elevated
			}
		}
		if co, ok := r.Values["co_ppm"].(float64); ok {
			if co > 5 {
				score -= 5 // Elevated CO
			}
		}
	}

	return max(score, 0)
}

// calculateStructuralScore computes structural risk
func (s *RiskService) calculateStructuralScore(readings []models.SensorReading, events []models.Event) float64 {
	score := 100.0

	// Check for structural events
	for _, event := range events {
		if event.EventType == "foundation_movement" || event.EventType == "crack_detected" {
			score -= 20
		}
	}

	// Analyze tilt readings
	for _, r := range readings {
		if tiltX, ok := r.Values["tilt_x"].(float64); ok {
			if math.Abs(tiltX) > 0.5 {
				score -= 10
			}
		}
		if crack, ok := r.Values["crack_displacement"].(float64); ok {
			if crack > 2.0 { // mm
				score -= 15
			}
		}
	}

	return max(score, 0)
}

// calculateHVACScore computes HVAC health
func (s *RiskService) calculateHVACScore(readings []models.SensorReading, events []models.Event) float64 {
	score := 100.0

	// Check efficiency
	for _, r := range readings {
		if eff, ok := r.Values["efficiency_score"].(float64); ok {
			if eff < 70 {
				score -= 25
			} else if eff < 85 {
				score -= 10
			}
		}
		if filterPressure, ok := r.Values["filter_pressure_drop"].(float64); ok {
			if filterPressure > 1.5 {
				score -= 15 // Clogged filter
			}
		}
	}

	return max(score, 0)
}

// calculateAirScore computes air quality score
func (s *RiskService) calculateAirScore(readings []models.SensorReading, events []models.Event) float64 {
	score := 100.0

	for _, r := range readings {
		if co2, ok := r.Values["co2_ppm"].(float64); ok {
			if co2 > 1000 {
				score -= 15
			} else if co2 > 800 {
				score -= 5
			}
		}
		if pm25, ok := r.Values["pm25"].(float64); ok {
			if pm25 > 35 {
				score -= 15 // Unhealthy
			} else if pm25 > 12 {
				score -= 5
			}
		}
		if voc, ok := r.Values["voc_index"].(float64); ok {
			if voc > 300 {
				score -= 10
			}
		}
	}

	return max(score, 0)
}

// calculateEnergyScore computes energy efficiency
func (s *RiskService) calculateEnergyScore(readings []models.SensorReading, events []models.Event) float64 {
	score := 100.0

	// Basic energy score - would be enhanced with Tesla data
	// Check for grid dependency, solar utilization, etc.

	return score
}

// calculateFireScore computes fire risk
func (s *RiskService) calculateFireScore(events []models.Event) float64 {
	score := 100.0

	for _, event := range events {
		if event.EventType == "smoke_detected" || event.EventType == "fire_alert" {
			score -= 40
		}
	}

	return max(score, 0)
}

// Helper functions

func groupReadingsByType(readings []models.SensorReading) map[string][]models.SensorReading {
	result := make(map[string][]models.SensorReading)
	for _, r := range readings {
		result[r.SensorType] = append(result[r.SensorType], r)
	}
	return result
}

func determineRiskTier(score float64) string {
	switch {
	case score >= 85:
		return "low"
	case score >= 70:
		return "medium"
	case score >= 50:
		return "high"
	default:
		return "critical"
	}
}

func calculateConfidence(readingCount int) float64 {
	switch {
	case readingCount < 100:
		return 0.5
	case readingCount < 500:
		return 0.7
	case readingCount < 1000:
		return 0.85
	default:
		return 0.95
	}
}

func average(values []float64) float64 {
	if len(values) == 0 {
		return 0
	}
	sum := 0.0
	for _, v := range values {
		sum += v
	}
	return sum / float64(len(values))
}

func stdDev(values []float64) float64 {
	if len(values) < 2 {
		return 0
	}
	avg := average(values)
	sumSquares := 0.0
	for _, v := range values {
		sumSquares += (v - avg) * (v - avg)
	}
	return math.Sqrt(sumSquares / float64(len(values)))
}

func max(a, b float64) float64 {
	if a > b {
		return a
	}
	return b
}
