# ALEXANDER one.1 Installation Guide

**Multi-Peril Smart Home Protection System**
**Version:** 1.1
**Date:** December 2025

---

## IMPORTANT SAFETY WARNINGS

**READ BEFORE INSTALLATION**

- Gas valve installation MUST be performed by a licensed plumber or gas technician
- Water valve installation MUST be performed by a licensed plumber
- Electrical connections MUST comply with local building codes
- This system is a SUPPLEMENT to, not a replacement for, standard safety devices
- Professional installation is STRONGLY RECOMMENDED

---

## Table of Contents

1. [Package Contents](#package-contents)
2. [System Requirements](#system-requirements)
3. [Pre-Installation Checklist](#pre-installation-checklist)
4. [Hardware Installation](#hardware-installation)
5. [Software Setup](#software-setup)
6. [Sensor Calibration](#sensor-calibration)
7. [Testing Procedures](#testing-procedures)
8. [Troubleshooting](#troubleshooting)

---

## Package Contents

### ALEXANDER one.1 Base Kit

| Item | Quantity | Description |
|------|----------|-------------|
| Control Hub | 1 | Raspberry Pi 4 with custom HAT |
| Water Pressure Sensor | 1 | Honeywell PX2 series |
| Water Shutoff Valve | 1 | Motorized ball valve, 3/4" |
| Gas Leak Sensor | 1 | MQ-4 methane detector |
| Smoke/CO Sensor | 1 | Photoelectric + electrochemical |
| Temperature/Humidity Sensor | 1 | DHT22 or SHT31 |
| Power Supply | 1 | 5V 3A USB-C |
| Mounting Hardware | 1 set | Screws, anchors, brackets |
| Quick Start Guide | 1 | This document |

### ALEXANDER one.1 Stove Safety Add-On (Sold Separately)

| Item | Quantity | Description |
|------|----------|-------------|
| IR Heat Sensor | 1 | MLX90614 infrared |
| PIR Motion Sensor | 1 | HC-SR501 |
| Gas Solenoid Valve | 1 | NC, CSA certified for gas |
| Mounting Bracket | 1 | Stove-mount kit |

---

## System Requirements

### Minimum Requirements

- WiFi network (2.4GHz or 5GHz)
- Smartphone (iOS 14+ or Android 10+)
- 120V AC power outlet within 6ft of hub location
- Water main accessible for valve installation
- Gas line accessible (if using gas features)

### Recommended

- Ethernet connection for hub (more reliable)
- UPS battery backup
- Professional installation

---

## Pre-Installation Checklist

Before starting, verify:

- [ ] Main water shutoff location identified
- [ ] Gas meter/shutoff location identified (if applicable)
- [ ] WiFi password available
- [ ] Smartphone charged and ready
- [ ] All package contents present
- [ ] Required tools available (see below)

### Tools Required

- Adjustable wrench
- Pipe wrench (for water valve)
- Screwdriver set (Phillips and flathead)
- Drill with masonry bits (if mounting to concrete)
- Teflon tape
- Multimeter (optional, for verification)
- Smartphone or tablet

---

## Hardware Installation

### Step 1: Control Hub Placement

**Location Requirements:**
- Central location in home
- Within WiFi range
- Away from heat sources
- Protected from water/moisture
- Accessible for maintenance

**Mounting:**
1. Use included bracket to mount hub on wall
2. Ensure ventilation slots are not blocked
3. Connect power supply
4. Wait for LED indicators (see LED guide below)

### Step 2: Water Pressure Sensor

**Location:** On main water line, after the main shutoff valve

**Installation:**
1. Turn OFF main water supply
2. Drain remaining water from pipes
3. Install T-fitting at main line
4. Connect pressure sensor to T-fitting
5. Apply Teflon tape to all threaded connections
6. Turn water back ON
7. Check for leaks
8. Route sensor cable to hub

**WARNING:** Improper installation can cause flooding. Professional installation recommended.

### Step 3: Water Shutoff Valve

**Location:** On main water line, after pressure sensor

**Installation:**
1. Turn OFF main water supply
2. Cut into main line (requires professional tools)
3. Install motorized ball valve
4. Connect electrical wires to hub (12V)
5. Test valve operation before sealing
6. Turn water back ON
7. Verify no leaks

**CRITICAL:** This valve controls your entire home's water supply. Professional installation is STRONGLY RECOMMENDED.

### Step 4: Gas Leak Sensor

**Location:** Within 6 feet of gas appliances, at appropriate height

- Natural gas: Mount HIGH (gas rises)
- Propane: Mount LOW (propane sinks)

**Installation:**
1. Mount sensor bracket on wall
2. Connect sensor to hub via included cable
3. Ensure sensor is not blocked by furniture/curtains
4. Avoid locations with excessive humidity

### Step 5: Smoke/CO Sensor

**Location:**
- One per floor minimum
- Outside each sleeping area
- In hallways
- NOT in kitchens or bathrooms (false alarms)

**Installation:**
1. Mount on ceiling or high on wall
2. Follow local fire code requirements
3. Connect to hub
4. Test with test button

### Step 6: Stove Safety System (Optional)

**IMPORTANT:** Gas valve installation MUST be performed by licensed professional.

**IR Heat Sensor:**
1. Mount 18-24 inches above stove surface
2. Angle sensor to view all burners
3. Secure with heat-resistant bracket

**Motion Sensor:**
1. Mount in kitchen to detect presence
2. Angle to cover stove area
3. Avoid pointing at windows (false triggers)

**Gas Solenoid Valve:**
1. MUST be installed by licensed gas technician
2. Install on gas line feeding stove
3. Ensure valve is CSA certified for gas
4. Test for leaks with soap solution

---

## Software Setup

### Step 1: Download App

- **iOS:** Search "ALEXANDER Home" in App Store
- **Android:** Search "ALEXANDER Home" in Google Play

### Step 2: Create Account

1. Open app
2. Tap "Create Account"
3. Enter email and create password
4. Verify email address

### Step 3: Add Hub

1. Tap "Add Device" → "ALEXANDER Hub"
2. Ensure hub is powered on (solid blue LED)
3. Follow in-app pairing instructions
4. Connect hub to your WiFi network

### Step 4: Add Sensors

1. Tap "Add Device" for each sensor
2. Follow on-screen instructions
3. Name each sensor by location (e.g., "Kitchen Gas Sensor")

### Step 5: Configure Alerts

1. Go to Settings → Notifications
2. Enable push notifications
3. Add emergency contacts (SMS alerts)
4. Configure alert thresholds

### Step 6: Enable Auto-Shutoff

1. Go to Settings → Safety Actions
2. Enable "Auto Water Shutoff"
3. Enable "Auto Gas Shutoff" (if applicable)
4. Set stove safety timeout (default: 5 minutes)

---

## Sensor Calibration

### Water Pressure Sensor

1. Go to Sensors → Water Pressure → Calibrate
2. Enter your normal water pressure (typically 40-60 PSI)
3. Set alert threshold (typically 30 PSI for leak detection)

### Gas Leak Sensor

1. Allow 24-48 hour burn-in period
2. Sensor auto-calibrates to ambient conditions
3. Test with commercial gas leak test spray (NOT actual gas)

### Stove Heat Sensor

1. Go to Sensors → Stove Heat → Calibrate
2. With stove OFF, tap "Set Baseline"
3. Turn on one burner to medium
4. After 2 minutes, tap "Set Active Threshold"

---

## Testing Procedures

### IMPORTANT: Test your system monthly

### Water Shutoff Test

1. Go to Controls → Water Valve
2. Tap "Test Shutoff"
3. System will close and reopen valve
4. Verify water stops and restarts

### Gas Shutoff Test (If Equipped)

1. Ensure all gas appliances are OFF
2. Go to Controls → Gas Valve
3. Tap "Test Shutoff"
4. Verify valve closes and reopens
5. Relight pilot lights if necessary

### Stove Safety Test

1. Turn on stove burner
2. Leave kitchen (go out of motion sensor range)
3. Wait for warning notification (3 minutes)
4. Return to kitchen before shutoff (5 minutes)
5. Verify warning was received

### Leak Detection Test

1. Go to Sensors → Water Pressure
2. Open a faucet fully
3. Verify pressure drop is detected
4. Close faucet

---

## LED Indicator Guide

| LED Color | Pattern | Meaning |
|-----------|---------|---------|
| Blue | Solid | Normal operation |
| Blue | Blinking | Connecting to WiFi |
| Green | Solid | Sensor reading normal |
| Yellow | Blinking | Warning condition |
| Red | Solid | Alert - action required |
| Red | Fast blink | Emergency - shutoff triggered |
| White | Blinking | Firmware update in progress |

---

## Troubleshooting

### Hub Won't Connect to WiFi

1. Ensure WiFi password is correct
2. Move hub closer to router
3. Try 2.4GHz network (not 5GHz)
4. Restart hub (unplug, wait 10 seconds, replug)

### Sensor Shows "Offline"

1. Check sensor cable connection
2. Verify hub is online
3. Try removing and re-adding sensor
4. Check for interference

### False Alarms

**Water Pressure:**
- Adjust threshold if normal pressure fluctuates
- Check for actual small leaks

**Gas Sensor:**
- Allow full 48-hour burn-in
- Move away from cooking areas
- Check for actual gas leaks

**Motion Sensor:**
- Adjust sensitivity in app
- Avoid pointing at heat sources, windows, or pets

### Valve Won't Operate

1. Check power connection
2. Verify valve isn't manually locked
3. Check for obstructions
4. Contact support if motor is burned out

---

## Support

**Website:** www.luxxhaus.com/support
**Email:** support@luxxhaus.com
**Phone:** 1-800-XXX-XXXX

**Emergency:** If you smell gas, leave immediately and call 911.

---

## Compliance

- FCC Part 15 Class B
- UL Listed (pending)
- CSA Certified (gas components)
- Designed to meet NFPA 72 guidelines

---

*ALEXANDER one.1 by PergoLuxx Construction*
*Patent Pending*
