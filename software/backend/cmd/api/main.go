s// cmd/api/main.go
// LUXX HAUS API Server - Main Entry Point
package main

import (
	"context"
	"log"
	"net/http"
	"os"
	"os/signal"
	"syscall"
	"time"

	"github.com/gin-gonic/gin"
	"github.com/joho/godotenv"
	"github.com/luxx-haus/api/internal/config"
	"github.com/luxx-haus/api/internal/handlers"
	"github.com/luxx-haus/api/internal/middleware"
	"github.com/luxx-haus/api/internal/repository"
	"github.com/luxx-haus/api/internal/services"
)

func main() {
	// Load .env file if present
	godotenv.Load()

	// Load configuration
	cfg := config.Load()

	// Initialize QuestDB connection
	db, err := repository.NewQuestDB(cfg.QuestDBHost, cfg.QuestDBPort, cfg.QuestDBUser, cfg.QuestDBPass)
	if err != nil {
		log.Fatalf("❌ Failed to connect to QuestDB: %v", err)
	}
	defer db.Close()
	log.Println("✅ Connected to QuestDB")

	// Initialize Redis cache
	cache, err := repository.NewRedis(cfg.RedisHost, cfg.RedisPort, cfg.RedisPass)
	if err != nil {
		log.Fatalf("❌ Failed to connect to Redis: %v", err)
	}
	defer cache.Close()
	log.Println("✅ Connected to Redis")

	// Initialize services
	riskService := services.NewRiskService(db)
	alertService := services.NewAlertService(db, cache)
	teslaService := services.NewTeslaService(cfg.TeslaClientID, cfg.TeslaClientSecret)

	// Initialize handlers
	h := handlers.New(db, cache, riskService, alertService, teslaService)

	// Setup Gin router
	if cfg.Environment == "production" {
		gin.SetMode(gin.ReleaseMode)
	}

	router := gin.New()
	router.Use(gin.Recovery())
	router.Use(middleware.Logger())
	router.Use(middleware.CORS())
	router.Use(middleware.SecurityHeaders())

	// Health check endpoints (no auth)
	router.GET("/health", h.HealthCheck)
	router.GET("/ready", h.ReadinessCheck)

	// API v1 routes (authenticated)
	v1 := router.Group("/api/v1")
	v1.Use(middleware.APIKeyAuth(db))
	v1.Use(middleware.RateLimit(cache, cfg.RateLimitRPS))
	{
		// Home endpoints
		homes := v1.Group("/homes")
		{
			homes.GET("/:policy_id/health", h.GetHomeHealth)
			homes.GET("/:policy_id/readings", h.GetReadings)
			homes.GET("/:policy_id/events", h.GetEvents)
			homes.GET("/:policy_id/predictions", h.GetPredictions)
			homes.GET("/:policy_id/tesla", h.GetTeslaStatus)
		}

		// Portfolio endpoints
		portfolio := v1.Group("/portfolio")
		{
			portfolio.GET("/risk", h.GetPortfolioRisk)
			portfolio.GET("/alerts", h.GetPortfolioAlerts)
			portfolio.GET("/summary", h.GetPortfolioSummary)
			portfolio.GET("/trends", h.GetPortfolioTrends)
		}

		// Claims endpoints
		claims := v1.Group("/claims")
		{
			claims.GET("/:event_id", h.GetClaimDocumentation)
			claims.GET("/prevented", h.GetPreventedClaims)
		}

		// Webhook management
		webhooks := v1.Group("/webhooks")
		{
			webhooks.POST("/subscribe", h.SubscribeWebhook)
			webhooks.DELETE("/unsubscribe", h.UnsubscribeWebhook)
			webhooks.GET("/subscriptions", h.ListWebhooks)
		}

		// Energy management (Tesla integration)
		energy := v1.Group("/energy")
		{
			energy.GET("/:home_id/usage", h.GetEnergyUsage)
			energy.GET("/:home_id/solar", h.GetSolarProduction)
			energy.GET("/:home_id/battery", h.GetBatteryStatus)
			energy.POST("/:home_id/mode", h.SetEnergyMode)
			energy.POST("/:home_id/backup-reserve", h.SetBackupReserve)
		}

		// Sensor management
		sensors := v1.Group("/sensors")
		{
			sensors.GET("/:home_id", h.ListSensors)
			sensors.GET("/:home_id/:sensor_id", h.GetSensor)
			sensors.POST("/:home_id/:sensor_id/command", h.SendSensorCommand)
		}
	}

	// Create HTTP server
	srv := &http.Server{
		Addr:         ":" + cfg.Port,
		Handler:      router,
		ReadTimeout:  15 * time.Second,
		WriteTimeout: 15 * time.Second,
		IdleTimeout:  60 * time.Second,
	}

	// Start server in goroutine
	go func() {
		log.Printf("🚀 LUXX HAUS API v2.0 starting on port %s", cfg.Port)
		log.Printf("📊 Environment: %s", cfg.Environment)
		if err := srv.ListenAndServe(); err != nil && err != http.ErrServerClosed {
			log.Fatalf("Server failed: %v", err)
		}
	}()

	// Graceful shutdown
	quit := make(chan os.Signal, 1)
	signal.Notify(quit, syscall.SIGINT, syscall.SIGTERM)
	<-quit

	log.Println("🛑 Shutting down server...")
	ctx, cancel := context.WithTimeout(context.Background(), 30*time.Second)
	defer cancel()

	if err := srv.Shutdown(ctx); err != nil {
		log.Fatalf("Server forced to shutdown: %v", err)
	}
	log.Println("✅ Server exited properly")
}
