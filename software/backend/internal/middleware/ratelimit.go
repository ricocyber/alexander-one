package middleware

import (
	"fmt"
	"net/http"
	"time"

	"github.com/gin-gonic/gin"
	"github.com/luxx-haus/api/internal/repository"
)

func RateLimit(cache *repository.Redis, defaultRPS int) gin.HandlerFunc {
	return func(c *gin.Context) {
		carrier := GetCarrier(c)
		if carrier == nil {
			c.Next()
			return
		}

		limit := getRateLimitForTier(carrier.Tier, defaultRPS)
		window := time.Second
		key := fmt.Sprintf("ratelimit:%s", carrier.CarrierID)

		allowed, remaining, err := cache.CheckRateLimit(c.Request.Context(), key, limit, window)
		if err != nil {
			c.Next()
			return
		}

		c.Header("X-RateLimit-Limit", fmt.Sprintf("%d", limit))
		c.Header("X-RateLimit-Remaining", fmt.Sprintf("%d", remaining))
		c.Header("X-RateLimit-Reset", fmt.Sprintf("%d", time.Now().Add(window).Unix()))

		if !allowed {
			c.Header("Retry-After", "1")
			c.AbortWithStatusJSON(http.StatusTooManyRequests, gin.H{
				"error":       "rate_limit_exceeded",
				"message":     "Too many requests",
				"retry_after": 1,
			})
			return
		}

		c.Next()
	}
}

func getRateLimitForTier(tier string, defaultRPS int) int {
	switch tier {
	case "enterprise":
		return 1000
	case "professional":
		return 500
	case "standard":
		return 100
	default:
		return defaultRPS
	}
}
