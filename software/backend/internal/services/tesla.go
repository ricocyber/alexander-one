// internal/services/tesla.go
// Tesla Fleet API integration for LUXX HAUS
package services

import (
	"context"
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"net/url"
	"strings"
	"sync"
	"time"

	"github.com/luxx-haus/api/internal/models"
)

const (
	teslaAuthURL  = "https://auth.tesla.com/oauth2/v3/token"
	teslaFleetURL = "https://fleet-api.prd.na.vn.cloud.tesla.com"
)

// TeslaService handles Tesla Fleet API integration
type TeslaService struct {
	clientID     string
	clientSecret string
	httpClient   *http.Client
	tokens       map[string]*tokenInfo
	mu           sync.RWMutex
}

type tokenInfo struct {
	AccessToken  string
	RefreshToken string
	ExpiresAt    time.Time
}

// NewTeslaService creates a new Tesla Fleet API client
func NewTeslaService(clientID, clientSecret string) *TeslaService {
	return &TeslaService{
		clientID:     clientID,
		clientSecret: clientSecret,
		httpClient: &http.Client{
			Timeout: 30 * time.Second,
		},
		tokens: make(map[string]*tokenInfo),
	}
}

// GetSiteStatus retrieves live status from a Tesla Energy site
func (t *TeslaService) GetSiteStatus(ctx context.Context, siteID string) (*models.TeslaStatus, error) {
	// Get valid token
	token, err := t.getToken(ctx, siteID)
	if err != nil {
		return nil, fmt.Errorf("failed to get token: %w", err)
	}

	// Get live status
	liveStatus, err := t.request(ctx, token, "GET", fmt.Sprintf("/api/1/energy_sites/%s/live_status", siteID), nil)
	if err != nil {
		return nil, fmt.Errorf("failed to get live status: %w", err)
	}

	// Get site info for backup reserve
	siteInfo, err := t.request(ctx, token, "GET", fmt.Sprintf("/api/1/energy_sites/%s/site_info", siteID), nil)
	if err != nil {
		// Non-fatal, continue with live status
		siteInfo = map[string]interface{}{}
	}

	status := &models.TeslaStatus{
		Connected:   true,
		SiteID:      siteID,
		LastUpdated: time.Now().UTC(),
	}

	// Parse live status
	if response, ok := liveStatus["response"].(map[string]interface{}); ok {
		if v, ok := response["solar_power"].(float64); ok {
			status.SolarPower = v
		}
		if v, ok := response["battery_power"].(float64); ok {
			status.BatteryPower = v
		}
		if v, ok := response["percentage_charged"].(float64); ok {
			status.BatterySOC = v
		}
		if v, ok := response["grid_power"].(float64); ok {
			status.GridPower = v
		}
		if v, ok := response["load_power"].(float64); ok {
			status.HomePower = v
		}
		if v, ok := response["grid_status"].(string); ok {
			status.GridStatus = v
		}
		if v, ok := response["storm_mode_active"].(bool); ok {
			status.StormWatch = v
		}
	}

	// Parse site info
	if response, ok := siteInfo["response"].(map[string]interface{}); ok {
		if v, ok := response["backup_reserve_percent"].(float64); ok {
			status.BackupReserve = v
		}
	}

	return status, nil
}

// SetOperationMode changes Powerwall operation mode
func (t *TeslaService) SetOperationMode(ctx context.Context, siteID string, mode string) error {
	token, err := t.getToken(ctx, siteID)
	if err != nil {
		return err
	}

	body := map[string]interface{}{
		"default_real_mode": mode,
	}

	_, err = t.request(ctx, token, "POST", fmt.Sprintf("/api/1/energy_sites/%s/operation", siteID), body)
	return err
}

// SetBackupReserve adjusts the backup reserve percentage
func (t *TeslaService) SetBackupReserve(ctx context.Context, siteID string, percent int) error {
	token, err := t.getToken(ctx, siteID)
	if err != nil {
		return err
	}

	body := map[string]interface{}{
		"backup_reserve_percent": percent,
	}

	_, err = t.request(ctx, token, "POST", fmt.Sprintf("/api/1/energy_sites/%s/backup", siteID), body)
	return err
}

// EnableStormWatch toggles storm watch mode
func (t *TeslaService) EnableStormWatch(ctx context.Context, siteID string, enabled bool) error {
	token, err := t.getToken(ctx, siteID)
	if err != nil {
		return err
	}

	body := map[string]interface{}{
		"enabled": enabled,
	}

	_, err = t.request(ctx, token, "POST", fmt.Sprintf("/api/1/energy_sites/%s/storm_mode", siteID), body)
	return err
}

// GetHistory retrieves historical energy data
func (t *TeslaService) GetHistory(ctx context.Context, siteID string, period string) (interface{}, error) {
	token, err := t.getToken(ctx, siteID)
	if err != nil {
		return nil, err
	}

	// Valid periods: day, week, month, year
	validPeriods := map[string]bool{"day": true, "week": true, "month": true, "year": true}
	if !validPeriods[period] {
		period = "day"
	}

	response, err := t.request(ctx, token, "GET", fmt.Sprintf("/api/1/energy_sites/%s/history?period=%s", siteID, period), nil)
	if err != nil {
		return nil, err
	}

	if data, ok := response["response"].(map[string]interface{}); ok {
		return data, nil
	}

	return response, nil
}

// getToken retrieves or refreshes an access token for a site
func (t *TeslaService) getToken(ctx context.Context, siteID string) (string, error) {
	t.mu.RLock()
	token, exists := t.tokens[siteID]
	t.mu.RUnlock()

	if exists && time.Now().Before(token.ExpiresAt.Add(-5*time.Minute)) {
		return token.AccessToken, nil
	}

	// Refresh or get new token
	newToken, err := t.refreshToken(ctx, siteID)
	if err != nil {
		return "", err
	}

	t.mu.Lock()
	t.tokens[siteID] = newToken
	t.mu.Unlock()

	return newToken.AccessToken, nil
}

// refreshToken gets a new access token using client credentials
func (t *TeslaService) refreshToken(ctx context.Context, siteID string) (*tokenInfo, error) {
	// For Partner Token authentication (machine-to-machine)
	data := url.Values{}
	data.Set("grant_type", "client_credentials")
	data.Set("client_id", t.clientID)
	data.Set("client_secret", t.clientSecret)
	data.Set("scope", "energy_device_data energy_cmds")
	data.Set("audience", teslaFleetURL)

	req, err := http.NewRequestWithContext(ctx, "POST", teslaAuthURL, strings.NewReader(data.Encode()))
	if err != nil {
		return nil, err
	}
	req.Header.Set("Content-Type", "application/x-www-form-urlencoded")

	resp, err := t.httpClient.Do(req)
	if err != nil {
		return nil, err
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusOK {
		body, _ := io.ReadAll(resp.Body)
		return nil, fmt.Errorf("token request failed: %s - %s", resp.Status, string(body))
	}

	var tokenResp struct {
		AccessToken  string `json:"access_token"`
		RefreshToken string `json:"refresh_token"`
		ExpiresIn    int    `json:"expires_in"`
		TokenType    string `json:"token_type"`
	}

	if err := json.NewDecoder(resp.Body).Decode(&tokenResp); err != nil {
		return nil, err
	}

	return &tokenInfo{
		AccessToken:  tokenResp.AccessToken,
		RefreshToken: tokenResp.RefreshToken,
		ExpiresAt:    time.Now().Add(time.Duration(tokenResp.ExpiresIn) * time.Second),
	}, nil
}

// request makes an authenticated request to Tesla Fleet API
func (t *TeslaService) request(ctx context.Context, token, method, path string, body interface{}) (map[string]interface{}, error) {
	var reqBody io.Reader
	if body != nil {
		jsonBody, err := json.Marshal(body)
		if err != nil {
			return nil, err
		}
		reqBody = strings.NewReader(string(jsonBody))
	}

	req, err := http.NewRequestWithContext(ctx, method, teslaFleetURL+path, reqBody)
	if err != nil {
		return nil, err
	}

	req.Header.Set("Authorization", "Bearer "+token)
	req.Header.Set("Content-Type", "application/json")

	resp, err := t.httpClient.Do(req)
	if err != nil {
		return nil, err
	}
	defer resp.Body.Close()

	if resp.StatusCode >= 400 {
		body, _ := io.ReadAll(resp.Body)
		return nil, fmt.Errorf("Tesla API error: %s - %s", resp.Status, string(body))
	}

	var result map[string]interface{}
	if err := json.NewDecoder(resp.Body).Decode(&result); err != nil {
		return nil, err
	}

	return result, nil
}
