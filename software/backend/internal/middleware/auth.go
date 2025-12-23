// internal/middleware/auth.go
// API Key authentication middleware for LUXX HAUS
package middleware

import (
	"context"
	"net/http"
	"strings"

	"github.com/gin-gonic/gin"
	"github.com/luxx-haus/api/internal/repository"
)

// CarrierContext key for storing carrier info in context
type contextKey string

const CarrierContextKey contextKey = "carrier"

// CarrierInfo stored in request context
type CarrierInfo struct {
	CarrierID string
	Tier      string
	HomeLimit int
}

// APIKeyAuth validates API key and sets carrier context
func APIKeyAuth(db *repository.QuestDB) gin.HandlerFunc {
	return func(c *gin.Context) {
		apiKey := extractAPIKey(c)
		if apiKey == "" {
			c.AbortWithStatusJSON(http.StatusUnauthorized, gin.H{
				"error":   "unauthorized",
				"message": "Missing API key. Provide via X-API-Key header or Authorization: Bearer <key>",
			})
			return
		}

		// Look up carrier by API key
		ctx := context.Background()
		carrier, err := db.GetCarrierByAPIKey(ctx, apiKey)
		if err != nil {
			c.AbortWithStatusJSON(http.StatusUnauthorized, gin.H{
				"error":   "unauthorized",
				"message": "Invalid API key",
			})
			return
		}

		if !carrier.Active {
			c.AbortWithStatusJSON(http.StatusForbidden, gin.H{
				"error":   "forbidden",
				"message": "Carrier account is inactive",
			})
			return
		}

		// Set carrier info in context
		carrierInfo := &CarrierInfo{
			CarrierID: carrier.CarrierID,
			Tier:      carrier.Tier,
			HomeLimit: carrier.HomeLimit,
		}
		c.Set(string(CarrierContextKey), carrierInfo)

		c.Next()
	}
}

// extractAPIKey gets API key from header
func extractAPIKey(c *gin.Context) string {
	// Check X-API-Key header first
	if key := c.GetHeader("X-API-Key"); key != "" {
		return key
	}

	// Check Authorization: Bearer header
	auth := c.GetHeader("Authorization")
	if auth != "" && strings.HasPrefix(auth, "Bearer ") {
		return strings.TrimPrefix(auth, "Bearer ")
	}

	return ""
}

// GetCarrier retrieves carrier info from context
func GetCarrier(c *gin.Context) *CarrierInfo {
	if carrier, exists := c.Get(string(CarrierContextKey)); exists {
		return carrier.(*CarrierInfo)
	}
	return nil
}
