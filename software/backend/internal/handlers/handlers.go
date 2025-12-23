// internal/handlers/handlers.go
// HTTP handlers for LUXX HAUS API
package handlers

import (
	"net/http"
	"strconv"
	"time"

	"github.com/gin-gonic/gin"
	"github.com/luxx-haus/api/internal/middleware"
	"github.com/luxx-haus/api/internal/models"
	"github.com/luxx-haus/api/internal/repository"
	"github.com/luxx-haus/api/internal/services"
)

// Handler contains all HTTP handlers
type Handler struct {
	db           *repository.QuestDB
	cache        *repository.Redis
	riskService  *services.RiskService
	alertService *services.AlertService
	teslaService *services.TeslaService
}

// New creates a new Handler
func New(
	db *repository.QuestDB,
	cache *repository.Redis,
	riskService *services.RiskService,
	alertService *services.AlertService,
	teslaService *services.TeslaService,
) *Handler {
	return &Handler{
		db:           db,
		cache:        cache,
		riskService:  riskService,
		alertService: alertService,
		teslaService: teslaService,
	}
}

// ============================================
// HEALTH CHECKS
// ============================================

// HealthCheck returns basic health status
func (h *Handler) HealthCheck(c *gin.Context) {
	c.JSON(http.StatusOK, gin.H{
		"status":  "healthy",
		"service": "luxx-haus-api",
		"version": "2.0.0",
		"time":    time.Now().UTC().Format(time.RFC3339),
	})
}

// ReadinessCheck verifies all dependencies are ready
func (h *Handler) ReadinessCheck(c *gin.Context) {
	ctx := c.Request.Context()

	// Check QuestDB
	dbReady := h.db.Ping(ctx) == nil

	// Check Redis
	cacheReady := h.cache.Ping(ctx) == nil

	if !dbReady || !cacheReady {
		c.JSON(http.StatusServiceUnavailable, gin.H{
			"status": "not_ready",
			"checks": gin.H{
				"questdb": dbReady,
				"redis":   cacheReady,
			},
		})
		return
	}

	c.JSON(http.StatusOK, gin.H{
		"status": "ready",
		"checks": gin.H{
			"questdb": true,
			"redis":   true,
		},
	})
}

// ============================================
// HOME ENDPOINTS
// ============================================

// GetHomeHealth returns comprehensive health data for a home
func (h *Handler) GetHomeHealth(c *gin.Context) {
	policyID := c.Param("policy_id")
	carrier := middleware.GetCarrier(c)
	ctx := c.Request.Context()

	// Get home by policy
	home, err := h.db.GetHomeByPolicy(ctx, carrier.CarrierID, policyID)
	if err != nil {
		c.JSON(http.StatusNotFound, gin.H{
			"error":   "not_found",
			"message": "Home not found for this policy",
		})
		return
	}

	// Get latest risk scores
	riskScores, err := h.db.GetLatestRiskScores(ctx, home.HomeID)
	if err != nil {
		riskScores = &models.RiskScores{OverallScore: home.HealthScore}
	}

	// Get recent events
	events, _ := h.db.GetRecentEvents(ctx, home.HomeID, 30)

	// Get active predictions
	predictions, _ := h.db.GetActivePredictions(ctx, home.HomeID)

	// Get claim stats
	claimStats, _ := h.db.GetClaimStats(ctx, home.HomeID, time.Now().Year())

	// Build response
	response := models.HomeHealthResponse{
		HomeID:       home.HomeID,
		PolicyNumber: home.PolicyNumber,
		Address:      home.Address + ", " + home.City + ", " + home.State + " " + home.Zip,
		HealthScore:  riskScores.OverallScore,
		RiskTier:     riskScores.RiskTier,
		LastReading:  home.LastReading,
		RiskBreakdown: models.RiskBreakdown{
			Water:      buildCategoryScore(riskScores.WaterScore, "water"),
			Gas:        buildCategoryScore(riskScores.GasScore, "gas"),
			Structural: buildCategoryScore(riskScores.StructuralScore, "structural"),
			HVAC:       buildCategoryScore(riskScores.HVACScore, "hvac"),
			Air:        buildCategoryScore(riskScores.AirScore, "air"),
			Energy:     buildCategoryScore(riskScores.EnergyScore, "energy"),
			Fire:       buildCategoryScore(riskScores.FireScore, "fire"),
		},
		Predictions:  predictions,
		RecentEvents: limitEvents(events, 10),
	}

	if claimStats != nil {
		response.ClaimsPrevented = claimStats.PreventedCount
		response.EstimatedSavings = claimStats.EstimatedSavings
	}

	// Add Tesla integration if available
	if home.TeslaSiteID.Valid {
		teslaStatus, err := h.teslaService.GetSiteStatus(ctx, home.TeslaSiteID.String)
		if err == nil {
			response.TeslaIntegration = teslaStatus
		}
	}

	c.JSON(http.StatusOK, response)
}

// GetReadings returns sensor readings for a home
func (h *Handler) GetReadings(c *gin.Context) {
	policyID := c.Param("policy_id")
	carrier := middleware.GetCarrier(c)
	ctx := c.Request.Context()

	// Get home
	home, err := h.db.GetHomeByPolicy(ctx, carrier.CarrierID, policyID)
	if err != nil {
		c.JSON(http.StatusNotFound, gin.H{"error": "not_found", "message": "Home not found"})
		return
	}

	// Parse query parameters
	filters := models.ReadingFilters{
		HomeID:     home.HomeID,
		SensorType: c.Query("sensor_type"),
		SensorID:   c.Query("sensor_id"),
		Limit:      100,
	}

	if limitStr := c.Query("limit"); limitStr != "" {
		if limit, err := strconv.Atoi(limitStr); err == nil && limit > 0 && limit <= 1000 {
			filters.Limit = limit
		}
	}

	if startStr := c.Query("start"); startStr != "" {
		if start, err := time.Parse(time.RFC3339, startStr); err == nil {
			filters.StartTime = start
		}
	}

	if endStr := c.Query("end"); endStr != "" {
		if end, err := time.Parse(time.RFC3339, endStr); err == nil {
			filters.EndTime = end
		}
	}

	// Get readings
	readings, err := h.db.GetSensorReadings(ctx, filters)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "database_error", "message": err.Error()})
		return
	}

	c.JSON(http.StatusOK, gin.H{
		"home_id":  home.HomeID,
		"count":    len(readings),
		"readings": readings,
	})
}

// GetEvents returns events for a home
func (h *Handler) GetEvents(c *gin.Context) {
	policyID := c.Param("policy_id")
	carrier := middleware.GetCarrier(c)
	ctx := c.Request.Context()

	home, err := h.db.GetHomeByPolicy(ctx, carrier.CarrierID, policyID)
	if err != nil {
		c.JSON(http.StatusNotFound, gin.H{"error": "not_found", "message": "Home not found"})
		return
	}

	days := 30
	if daysStr := c.Query("days"); daysStr != "" {
		if d, err := strconv.Atoi(daysStr); err == nil && d > 0 && d <= 365 {
			days = d
		}
	}

	events, err := h.db.GetRecentEvents(ctx, home.HomeID, days)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "database_error", "message": err.Error()})
		return
	}

	c.JSON(http.StatusOK, gin.H{
		"home_id": home.HomeID,
		"days":    days,
		"count":   len(events),
		"events":  events,
	})
}

// GetPredictions returns ML predictions for a home
func (h *Handler) GetPredictions(c *gin.Context) {
	policyID := c.Param("policy_id")
	carrier := middleware.GetCarrier(c)
	ctx := c.Request.Context()

	home, err := h.db.GetHomeByPolicy(ctx, carrier.CarrierID, policyID)
	if err != nil {
		c.JSON(http.StatusNotFound, gin.H{"error": "not_found", "message": "Home not found"})
		return
	}

	predictions, err := h.db.GetActivePredictions(ctx, home.HomeID)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "database_error", "message": err.Error()})
		return
	}

	c.JSON(http.StatusOK, gin.H{
		"home_id":     home.HomeID,
		"count":       len(predictions),
		"predictions": predictions,
	})
}

// GetTeslaStatus returns Tesla Powerwall status for a home
func (h *Handler) GetTeslaStatus(c *gin.Context) {
	policyID := c.Param("policy_id")
	carrier := middleware.GetCarrier(c)
	ctx := c.Request.Context()

	home, err := h.db.GetHomeByPolicy(ctx, carrier.CarrierID, policyID)
	if err != nil {
		c.JSON(http.StatusNotFound, gin.H{"error": "not_found", "message": "Home not found"})
		return
	}

	if !home.TeslaSiteID.Valid {
		c.JSON(http.StatusNotFound, gin.H{
			"error":   "not_configured",
			"message": "Tesla integration not configured for this home",
		})
		return
	}

	status, err := h.teslaService.GetSiteStatus(ctx, home.TeslaSiteID.String)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "tesla_error", "message": err.Error()})
		return
	}

	c.JSON(http.StatusOK, status)
}

// ============================================
// HELPER FUNCTIONS
// ============================================

func buildCategoryScore(score float64, category string) models.CategoryScore {
	trend := "stable"
	if score >= 90 {
		trend = "improving"
	} else if score < 70 {
		trend = "declining"
	}

	return models.CategoryScore{
		Score:   score,
		Trend:   trend,
		Factors: []models.RiskFactor{}, // Would be populated by risk service
	}
}

func limitEvents(events []models.Event, max int) []models.Event {
	if len(events) <= max {
		return events
	}
	return events[:max]
}
