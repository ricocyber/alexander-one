// internal/handlers/portfolio.go
// Portfolio and Claims handlers for LUXX HAUS API
package handlers

import (
	"net/http"
	"time"

	"github.com/gin-gonic/gin"
	"github.com/luxx-haus/api/internal/middleware"
)

// ============================================
// PORTFOLIO ENDPOINTS
// ============================================

// GetPortfolioRisk returns aggregate portfolio risk for a carrier
func (h *Handler) GetPortfolioRisk(c *gin.Context) {
	carrier := middleware.GetCarrier(c)
	ctx := c.Request.Context()

	// Get portfolio stats
	portfolio, err := h.db.GetPortfolioStats(ctx, carrier.CarrierID)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{
			"error":   "database_error",
			"message": err.Error(),
		})
		return
	}

	// Get high risk homes
	highRiskHomes, _ := h.db.GetHighRiskHomes(ctx, carrier.CarrierID, 10)
	portfolio.HighRiskHomes = highRiskHomes

	// Determine trend direction based on recent score changes
	portfolio.TrendDirection = "stable" // Would calculate from historical data

	c.JSON(http.StatusOK, portfolio)
}

// GetPortfolioAlerts returns recent alerts across all homes
func (h *Handler) GetPortfolioAlerts(c *gin.Context) {
	carrier := middleware.GetCarrier(c)
	ctx := c.Request.Context()

	// Get all homes for carrier
	homes, err := h.db.GetHomesByCarrier(ctx, carrier.CarrierID)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "database_error", "message": err.Error()})
		return
	}

	// Collect alerts from all homes
	var allAlerts []map[string]interface{}
	for _, home := range homes {
		events, _ := h.db.GetRecentEvents(ctx, home.HomeID, 1) // Last 24 hours
		for _, event := range events {
			if event.Severity == "critical" || event.Severity == "warning" {
				allAlerts = append(allAlerts, map[string]interface{}{
					"event_id":      event.EventID,
					"home_id":       home.HomeID,
					"policy_number": home.PolicyNumber,
					"address":       home.Address,
					"event_type":    event.EventType,
					"severity":      event.Severity,
					"description":   event.Description,
					"timestamp":     event.Timestamp,
					"resolved":      event.Resolved,
				})
			}
		}
	}

	c.JSON(http.StatusOK, gin.H{
		"carrier_id":   carrier.CarrierID,
		"total_alerts": len(allAlerts),
		"alerts":       allAlerts,
		"generated_at": time.Now().UTC(),
	})
}

// GetPortfolioSummary returns summary statistics
func (h *Handler) GetPortfolioSummary(c *gin.Context) {
	carrier := middleware.GetCarrier(c)
	ctx := c.Request.Context()

	portfolio, err := h.db.GetPortfolioStats(ctx, carrier.CarrierID)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "database_error", "message": err.Error()})
		return
	}

	c.JSON(http.StatusOK, gin.H{
		"carrier_id":        carrier.CarrierID,
		"total_homes":       portfolio.TotalHomes,
		"active_homes":      portfolio.ActiveHomes,
		"average_score":     portfolio.AverageScore,
		"risk_distribution": portfolio.RiskDistribution,
		"claims_prevented":  portfolio.ClaimsPrevented,
		"savings_ytd":       portfolio.EstimatedSavings,
		"generated_at":      time.Now().UTC(),
	})
}

// GetPortfolioTrends returns historical trends
func (h *Handler) GetPortfolioTrends(c *gin.Context) {
	carrier := middleware.GetCarrier(c)

	// Placeholder - would query historical aggregates
	c.JSON(http.StatusOK, gin.H{
		"carrier_id": carrier.CarrierID,
		"period":     "30d",
		"trends": gin.H{
			"average_score": gin.H{
				"current":  82.5,
				"previous": 80.2,
				"change":   2.3,
			},
			"claims_prevented": gin.H{
				"current":  15,
				"previous": 12,
				"change":   3,
			},
			"high_risk_homes": gin.H{
				"current":  8,
				"previous": 11,
				"change":   -3,
			},
		},
		"generated_at": time.Now().UTC(),
	})
}

// ============================================
// CLAIMS ENDPOINTS
// ============================================

// GetClaimDocumentation returns full claim documentation package
func (h *Handler) GetClaimDocumentation(c *gin.Context) {
	eventID := c.Param("event_id")
	carrier := middleware.GetCarrier(c)
	ctx := c.Request.Context()

	// This would retrieve comprehensive claim documentation
	// including sensor readings before/during/after the event

	_ = carrier // Would verify carrier owns this event
	_ = ctx

	// Placeholder response structure
	c.JSON(http.StatusOK, gin.H{
		"claim_id":      "CLM-" + eventID,
		"event_id":      eventID,
		"status":        "documented",
		"timeline":      []map[string]interface{}{},
		"sensor_data":   gin.H{},
		"automated_response": gin.H{
			"action":    "valve_closed",
			"timestamp": time.Now().Add(-1 * time.Hour).UTC(),
		},
		"outcome":           "claim_prevented",
		"estimated_savings": 15000.00,
		"generated_at":      time.Now().UTC(),
	})
}

// GetPreventedClaims returns list of prevented claims
func (h *Handler) GetPreventedClaims(c *gin.Context) {
	carrier := middleware.GetCarrier(c)
	ctx := c.Request.Context()

	homes, err := h.db.GetHomesByCarrier(ctx, carrier.CarrierID)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "database_error", "message": err.Error()})
		return
	}

	var preventedClaims []map[string]interface{}
	var totalSavings float64

	for _, home := range homes {
		events, _ := h.db.GetRecentEvents(ctx, home.HomeID, 365)
		for _, event := range events {
			if event.ClaimPrevented {
				preventedClaims = append(preventedClaims, map[string]interface{}{
					"event_id":         event.EventID,
					"home_id":          home.HomeID,
					"policy_number":    home.PolicyNumber,
					"event_type":       event.EventType,
					"timestamp":        event.Timestamp,
					"automated_action": event.AutomatedAction,
					"estimated_savings": event.EstimatedSavings,
				})
				totalSavings += event.EstimatedSavings
			}
		}
	}

	c.JSON(http.StatusOK, gin.H{
		"carrier_id":     carrier.CarrierID,
		"period":         "ytd",
		"total_prevented": len(preventedClaims),
		"total_savings":  totalSavings,
		"claims":         preventedClaims,
		"generated_at":   time.Now().UTC(),
	})
}

// ============================================
// WEBHOOK ENDPOINTS
// ============================================

// SubscribeWebhook creates a webhook subscription
func (h *Handler) SubscribeWebhook(c *gin.Context) {
	carrier := middleware.GetCarrier(c)

	var req struct {
		URL    string   `json:"url" binding:"required"`
		Events []string `json:"events" binding:"required"`
	}

	if err := c.ShouldBindJSON(&req); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": "invalid_request", "message": err.Error()})
		return
	}

	// Validate events
	validEvents := map[string]bool{
		"leak_detected":    true,
		"gas_alert":        true,
		"critical_risk":    true,
		"hvac_failure":     true,
		"structural_alert": true,
		"all":              true,
	}

	for _, event := range req.Events {
		if !validEvents[event] {
			c.JSON(http.StatusBadRequest, gin.H{
				"error":   "invalid_event",
				"message": "Invalid event type: " + event,
			})
			return
		}
	}

	// Create subscription (would store in database)
	subscriptionID := "sub_" + time.Now().Format("20060102150405")

	c.JSON(http.StatusCreated, gin.H{
		"subscription_id": subscriptionID,
		"carrier_id":      carrier.CarrierID,
		"url":             req.URL,
		"events":          req.Events,
		"active":          true,
		"created_at":      time.Now().UTC(),
	})
}

// UnsubscribeWebhook removes a webhook subscription
func (h *Handler) UnsubscribeWebhook(c *gin.Context) {
	subscriptionID := c.Query("subscription_id")
	if subscriptionID == "" {
		c.JSON(http.StatusBadRequest, gin.H{"error": "missing_parameter", "message": "subscription_id required"})
		return
	}

	// Would delete from database
	c.JSON(http.StatusOK, gin.H{
		"subscription_id": subscriptionID,
		"status":          "deleted",
	})
}

// ListWebhooks returns all webhook subscriptions for a carrier
func (h *Handler) ListWebhooks(c *gin.Context) {
	carrier := middleware.GetCarrier(c)

	// Would query from database
	c.JSON(http.StatusOK, gin.H{
		"carrier_id":    carrier.CarrierID,
		"subscriptions": []map[string]interface{}{},
	})
}
