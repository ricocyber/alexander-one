// internal/handlers/energy.go
// Energy and Sensor handlers for LUXX HAUS API
package handlers

import (
	"net/http"
	"time"

	"github.com/gin-gonic/gin"
	"github.com/luxx-haus/api/internal/middleware"
)

// ============================================
// ENERGY ENDPOINTS (Tesla Integration)
// ============================================

// GetEnergyUsage returns energy usage patterns
func (h *Handler) GetEnergyUsage(c *gin.Context) {
	homeID := c.Param("home_id")
	carrier := middleware.GetCarrier(c)
	ctx := c.Request.Context()

	// Verify home belongs to carrier
	home, err := h.db.GetHomeByID(ctx, homeID)
	if err != nil || home.CarrierID != carrier.CarrierID {
		c.JSON(http.StatusNotFound, gin.H{"error": "not_found", "message": "Home not found"})
		return
	}

	if !home.TeslaSiteID.Valid {
		c.JSON(http.StatusNotFound, gin.H{"error": "not_configured", "message": "Tesla not configured"})
		return
	}

	// Get energy history from Tesla
	period := c.DefaultQuery("period", "day")
	history, err := h.teslaService.GetHistory(ctx, home.TeslaSiteID.String, period)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "tesla_error", "message": err.Error()})
		return
	}

	c.JSON(http.StatusOK, gin.H{
		"home_id": homeID,
		"period":  period,
		"usage":   history,
	})
}

// GetSolarProduction returns solar production data
func (h *Handler) GetSolarProduction(c *gin.Context) {
	homeID := c.Param("home_id")
	carrier := middleware.GetCarrier(c)
	ctx := c.Request.Context()

	home, err := h.db.GetHomeByID(ctx, homeID)
	if err != nil || home.CarrierID != carrier.CarrierID {
		c.JSON(http.StatusNotFound, gin.H{"error": "not_found", "message": "Home not found"})
		return
	}

	if !home.TeslaSiteID.Valid {
		c.JSON(http.StatusNotFound, gin.H{"error": "not_configured", "message": "Tesla not configured"})
		return
	}

	status, err := h.teslaService.GetSiteStatus(ctx, home.TeslaSiteID.String)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "tesla_error", "message": err.Error()})
		return
	}

	c.JSON(http.StatusOK, gin.H{
		"home_id":      homeID,
		"solar_power":  status.SolarPower,
		"last_updated": status.LastUpdated,
	})
}

// GetBatteryStatus returns Powerwall battery status
func (h *Handler) GetBatteryStatus(c *gin.Context) {
	homeID := c.Param("home_id")
	carrier := middleware.GetCarrier(c)
	ctx := c.Request.Context()

	home, err := h.db.GetHomeByID(ctx, homeID)
	if err != nil || home.CarrierID != carrier.CarrierID {
		c.JSON(http.StatusNotFound, gin.H{"error": "not_found", "message": "Home not found"})
		return
	}

	if !home.TeslaSiteID.Valid {
		c.JSON(http.StatusNotFound, gin.H{"error": "not_configured", "message": "Tesla not configured"})
		return
	}

	status, err := h.teslaService.GetSiteStatus(ctx, home.TeslaSiteID.String)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "tesla_error", "message": err.Error()})
		return
	}

	c.JSON(http.StatusOK, gin.H{
		"home_id":        homeID,
		"battery_soc":    status.BatterySOC,
		"battery_power":  status.BatteryPower,
		"backup_reserve": status.BackupReserve,
		"storm_watch":    status.StormWatch,
		"grid_status":    status.GridStatus,
		"last_updated":   status.LastUpdated,
	})
}

// SetEnergyMode changes Powerwall operation mode
func (h *Handler) SetEnergyMode(c *gin.Context) {
	homeID := c.Param("home_id")
	carrier := middleware.GetCarrier(c)
	ctx := c.Request.Context()

	home, err := h.db.GetHomeByID(ctx, homeID)
	if err != nil || home.CarrierID != carrier.CarrierID {
		c.JSON(http.StatusNotFound, gin.H{"error": "not_found", "message": "Home not found"})
		return
	}

	if !home.TeslaSiteID.Valid {
		c.JSON(http.StatusNotFound, gin.H{"error": "not_configured", "message": "Tesla not configured"})
		return
	}

	var req struct {
		Mode string `json:"mode" binding:"required"` // self_consumption, backup, autonomous
	}

	if err := c.ShouldBindJSON(&req); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": "invalid_request", "message": err.Error()})
		return
	}

	validModes := map[string]bool{
		"self_consumption": true,
		"backup":           true,
		"autonomous":       true,
		"time_based":       true,
	}

	if !validModes[req.Mode] {
		c.JSON(http.StatusBadRequest, gin.H{"error": "invalid_mode", "message": "Valid modes: self_consumption, backup, autonomous, time_based"})
		return
	}

	err = h.teslaService.SetOperationMode(ctx, home.TeslaSiteID.String, req.Mode)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "tesla_error", "message": err.Error()})
		return
	}

	c.JSON(http.StatusOK, gin.H{
		"home_id": homeID,
		"mode":    req.Mode,
		"status":  "updated",
	})
}

// SetBackupReserve adjusts Powerwall backup reserve
func (h *Handler) SetBackupReserve(c *gin.Context) {
	homeID := c.Param("home_id")
	carrier := middleware.GetCarrier(c)
	ctx := c.Request.Context()

	home, err := h.db.GetHomeByID(ctx, homeID)
	if err != nil || home.CarrierID != carrier.CarrierID {
		c.JSON(http.StatusNotFound, gin.H{"error": "not_found", "message": "Home not found"})
		return
	}

	if !home.TeslaSiteID.Valid {
		c.JSON(http.StatusNotFound, gin.H{"error": "not_configured", "message": "Tesla not configured"})
		return
	}

	var req struct {
		Percent int `json:"percent" binding:"required,min=0,max=100"`
	}

	if err := c.ShouldBindJSON(&req); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": "invalid_request", "message": err.Error()})
		return
	}

	err = h.teslaService.SetBackupReserve(ctx, home.TeslaSiteID.String, req.Percent)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "tesla_error", "message": err.Error()})
		return
	}

	c.JSON(http.StatusOK, gin.H{
		"home_id":        homeID,
		"backup_reserve": req.Percent,
		"status":         "updated",
	})
}

// ============================================
// SENSOR ENDPOINTS
// ============================================

// ListSensors returns all sensors for a home
func (h *Handler) ListSensors(c *gin.Context) {
	homeID := c.Param("home_id")
	carrier := middleware.GetCarrier(c)
	ctx := c.Request.Context()

	home, err := h.db.GetHomeByID(ctx, homeID)
	if err != nil || home.CarrierID != carrier.CarrierID {
		c.JSON(http.StatusNotFound, gin.H{"error": "not_found", "message": "Home not found"})
		return
	}

	sensors, err := h.db.GetSensorsByHome(ctx, homeID)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "database_error", "message": err.Error()})
		return
	}

	c.JSON(http.StatusOK, gin.H{
		"home_id": homeID,
		"count":   len(sensors),
		"sensors": sensors,
	})
}

// GetSensor returns a specific sensor
func (h *Handler) GetSensor(c *gin.Context) {
	homeID := c.Param("home_id")
	sensorID := c.Param("sensor_id")
	carrier := middleware.GetCarrier(c)
	ctx := c.Request.Context()

	home, err := h.db.GetHomeByID(ctx, homeID)
	if err != nil || home.CarrierID != carrier.CarrierID {
		c.JSON(http.StatusNotFound, gin.H{"error": "not_found", "message": "Home not found"})
		return
	}

	sensors, err := h.db.GetSensorsByHome(ctx, homeID)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "database_error", "message": err.Error()})
		return
	}

	for _, sensor := range sensors {
		if sensor.SensorID == sensorID {
			c.JSON(http.StatusOK, sensor)
			return
		}
	}

	c.JSON(http.StatusNotFound, gin.H{"error": "not_found", "message": "Sensor not found"})
}

// SendSensorCommand sends a command to a sensor
func (h *Handler) SendSensorCommand(c *gin.Context) {
	homeID := c.Param("home_id")
	sensorID := c.Param("sensor_id")
	carrier := middleware.GetCarrier(c)
	ctx := c.Request.Context()

	home, err := h.db.GetHomeByID(ctx, homeID)
	if err != nil || home.CarrierID != carrier.CarrierID {
		c.JSON(http.StatusNotFound, gin.H{"error": "not_found", "message": "Home not found"})
		return
	}

	var req struct {
		Command string                 `json:"command" binding:"required"` // close_valve, open_valve, calibrate, reboot
		Params  map[string]interface{} `json:"params"`
	}

	if err := c.ShouldBindJSON(&req); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": "invalid_request", "message": err.Error()})
		return
	}

	validCommands := map[string]bool{
		"close_valve": true,
		"open_valve":  true,
		"calibrate":   true,
		"reboot":      true,
		"test_alert":  true,
	}

	if !validCommands[req.Command] {
		c.JSON(http.StatusBadRequest, gin.H{"error": "invalid_command", "message": "Unknown command"})
		return
	}

	// Would publish to MQTT topic: luxx/{home_id}/commands/sensor/{sensor_id}
	_ = ctx

	c.JSON(http.StatusAccepted, gin.H{
		"home_id":    homeID,
		"sensor_id":  sensorID,
		"command":    req.Command,
		"status":     "sent",
		"message_id": "msg_" + time.Now().Format("20060102150405"),
	})
}
