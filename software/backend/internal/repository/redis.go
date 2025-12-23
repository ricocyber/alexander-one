// internal/repository/redis.go
// Redis client for caching and rate limiting
package repository

import (
	"context"
	"encoding/json"
	"fmt"
	"time"

	"github.com/redis/go-redis/v9"
)

// Redis wraps the Redis client
type Redis struct {
	client *redis.Client
}

// NewRedis creates a new Redis connection
func NewRedis(host string, port int, password string) (*Redis, error) {
	client := redis.NewClient(&redis.Options{
		Addr:         fmt.Sprintf("%s:%d", host, port),
		Password:     password,
		DB:           0,
		PoolSize:     100,
		MinIdleConns: 10,
		DialTimeout:  5 * time.Second,
		ReadTimeout:  3 * time.Second,
		WriteTimeout: 3 * time.Second,
	})

	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel()

	if err := client.Ping(ctx).Err(); err != nil {
		return nil, fmt.Errorf("failed to connect to Redis: %w", err)
	}

	return &Redis{client: client}, nil
}

// Close closes the Redis connection
func (r *Redis) Close() error {
	return r.client.Close()
}

// Ping checks Redis connectivity
func (r *Redis) Ping(ctx context.Context) error {
	return r.client.Ping(ctx).Err()
}

// CheckRateLimit implements sliding window rate limiting
func (r *Redis) CheckRateLimit(ctx context.Context, key string, limit int, window time.Duration) (bool, int, error) {
	now := time.Now()
	windowStart := now.Add(-window)

	pipe := r.client.Pipeline()
	pipe.ZRemRangeByScore(ctx, key, "0", fmt.Sprintf("%d", windowStart.UnixNano()))
	countCmd := pipe.ZCard(ctx, key)
	pipe.ZAdd(ctx, key, redis.Z{
		Score:  float64(now.UnixNano()),
		Member: fmt.Sprintf("%d", now.UnixNano()),
	})
	pipe.Expire(ctx, key, window)

	_, err := pipe.Exec(ctx)
	if err != nil {
		return false, 0, err
	}

	count := int(countCmd.Val())
	remaining := limit - count - 1
	if remaining < 0 {
		remaining = 0
	}

	return count < limit, remaining, nil
}

// Set stores a value with expiration
func (r *Redis) Set(ctx context.Context, key string, value interface{}, exp time.Duration) error {
	data, err := json.Marshal(value)
	if err != nil {
		return err
	}
	return r.client.Set(ctx, key, data, exp).Err()
}

// Get retrieves a value
func (r *Redis) Get(ctx context.Context, key string, dest interface{}) error {
	data, err := r.client.Get(ctx, key).Bytes()
	if err != nil {
		return err
	}
	return json.Unmarshal(data, dest)
}

// Delete removes a key
func (r *Redis) Delete(ctx context.Context, key string) error {
	return r.client.Del(ctx, key).Err()
}

// Exists checks if key exists
func (r *Redis) Exists(ctx context.Context, key string) (bool, error) {
	n, err := r.client.Exists(ctx, key).Result()
	return n > 0, err
}

// CacheHomeHealth stores home health data
func (r *Redis) CacheHomeHealth(ctx context.Context, homeID string, data interface{}) error {
	return r.Set(ctx, fmt.Sprintf("home:health:%s", homeID), data, 5*time.Minute)
}

// GetCachedHomeHealth retrieves cached home health
func (r *Redis) GetCachedHomeHealth(ctx context.Context, homeID string, dest interface{}) error {
	return r.Get(ctx, fmt.Sprintf("home:health:%s", homeID), dest)
}

// CacheTeslaStatus stores Tesla status
func (r *Redis) CacheTeslaStatus(ctx context.Context, siteID string, data interface{}) error {
	return r.Set(ctx, fmt.Sprintf("tesla:%s", siteID), data, 30*time.Second)
}

// GetCachedTeslaStatus retrieves Tesla status
func (r *Redis) GetCachedTeslaStatus(ctx context.Context, siteID string, dest interface{}) error {
	return r.Get(ctx, fmt.Sprintf("tesla:%s", siteID), dest)
}

// CachePortfolioStats stores portfolio stats
func (r *Redis) CachePortfolioStats(ctx context.Context, carrierID string, data interface{}) error {
	return r.Set(ctx, fmt.Sprintf("portfolio:%s", carrierID), data, 10*time.Minute)
}

// GetCachedPortfolioStats retrieves portfolio stats
func (r *Redis) GetCachedPortfolioStats(ctx context.Context, carrierID string, dest interface{}) error {
	return r.Get(ctx, fmt.Sprintf("portfolio:%s", carrierID), dest)
}

// SetAlertSent marks alert as sent
func (r *Redis) SetAlertSent(ctx context.Context, alertKey string, ttl time.Duration) error {
	return r.client.Set(ctx, fmt.Sprintf("alert:%s", alertKey), "1", ttl).Err()
}

// WasAlertSent checks if alert was sent
func (r *Redis) WasAlertSent(ctx context.Context, alertKey string) (bool, error) {
	return r.Exists(ctx, fmt.Sprintf("alert:%s", alertKey))
}

// PublishEvent publishes to Redis pubsub
func (r *Redis) PublishEvent(ctx context.Context, channel string, event interface{}) error {
	data, err := json.Marshal(event)
	if err != nil {
		return err
	}
	return r.client.Publish(ctx, channel, data).Err()
}
