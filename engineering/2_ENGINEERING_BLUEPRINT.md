# ALEXANDER ONE - ENGINEERING BLUEPRINT
## Complete Technical Specification for Development

**Version:** 1.1 "Sentinel"
**Prepared for:** Joe Hobart, Firmware Engineer
**Date:** December 2025

---

# TABLE OF CONTENTS

1. System Architecture
2. Device Specifications (7 Devices)
3. Build vs Buy Matrix
4. Communication Protocols
5. Firmware Requirements
6. Power Architecture
7. Bill of Materials
8. Development Phases
9. Open Questions for Discussion

---

# 1. SYSTEM ARCHITECTURE

```
                    ALEXANDER ONE SYSTEM TOPOLOGY

    ┌─────────────────────────────────────────────────────────────────┐
    │                         SENSOR LAYER                            │
    ├─────────────────────────────────────────────────────────────────┤
    │                                                                 │
    │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐           │
    │  │  LEAK    │ │   AIR    │ │   GAS    │ │  HVAC    │           │
    │  │  SPOT    │ │  SENSOR  │ │ GUARDIAN │ │ SENTINEL │           │
    │  │          │ │          │ │          │ │          │           │
    │  │ ESP32-C6 │ │ ESP32-C6 │ │ ESP32-C6 │ │ ESP32-C6 │           │
    │  │ Zigbee   │ │ Zigbee   │ │ Zigbee   │ │ Zigbee   │           │
    │  └────┬─────┘ └────┬─────┘ └────┬─────┘ └────┬─────┘           │
    │       │            │            │            │                  │
    │       └────────────┴─────┬──────┴────────────┘                  │
    │                          │                                      │
    │                    ZIGBEE 3.0 MESH                              │
    │                          │                                      │
    │  ┌──────────┐            │            ┌──────────┐              │
    │  │FOUNDATION│            │            │  WATER   │              │
    │  │ SENSOR   │            │            │ GUARDIAN │              │
    │  │          │            │            │          │              │
    │  │ ESP32    │            │            │ ESP32-C6 │              │
    │  │ LoRa     │            │            │ Zigbee   │              │
    │  └────┬─────┘            │            └────┬─────┘              │
    │       │                  │                 │                    │
    │       │LoRa 915MHz       │                 │                    │
    │       │                  │                 │                    │
    └───────┼──────────────────┼─────────────────┼────────────────────┘
            │                  │                 │
            │                  ▼                 │
    ┌───────┴──────────────────────────────────┴──────────────────────┐
    │                                                                  │
    │                      ALEXANDER HUB 1.1                           │
    │                      (THE BRAIN)                                 │
    │                                                                  │
    │  ┌─────────────────────────────────────────────────────────────┐│
    │  │                                                             ││
    │  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐    ││
    │  │  │ ZIGBEE   │  │  WiFi 6  │  │   LoRa   │  │   LTE    │    ││
    │  │  │CC2652P7  │  │ ESP32-S3 │  │  SX1262  │  │   BG96   │    ││
    │  │  │Coordinator│ │          │  │ 915MHz   │  │ Cat-M1   │    ││
    │  │  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘    ││
    │  │       │             │             │             │          ││
    │  │       └─────────────┴──────┬──────┴─────────────┘          ││
    │  │                            │                               ││
    │  │                     ┌──────▼──────┐                        ││
    │  │                     │  RPi CM4    │                        ││
    │  │                     │  4GB/32GB   │                        ││
    │  │                     │             │                        ││
    │  │                     │ TensorFlow  │                        ││
    │  │                     │  XGBoost    │                        ││
    │  │                     │  Yocto OS   │                        ││
    │  │                     └──────┬──────┘                        ││
    │  │                            │                               ││
    │  │           ┌────────────────┼────────────────┐              ││
    │  │           │                │                │              ││
    │  │      ┌────▼────┐     ┌─────▼─────┐    ┌────▼────┐         ││
    │  │      │ 7" LCD  │     │  SENSORS  │    │ BATTERY │         ││
    │  │      │ Touch   │     │ PM/CO2/VOC│    │ 8 Hour  │         ││
    │  │      └─────────┘     └───────────┘    └─────────┘         ││
    │  │                                                             ││
    │  └─────────────────────────────────────────────────────────────┘│
    │                                                                  │
    └──────────────────────────────────────────────────────────────────┘
                                    │
                                    │ WiFi / LTE
                                    ▼
    ┌──────────────────────────────────────────────────────────────────┐
    │                         CLOUD / API LAYER                        │
    ├──────────────────────────────────────────────────────────────────┤
    │                                                                  │
    │   ┌──────────────┐   ┌──────────────┐   ┌──────────────┐        │
    │   │ TESLA FLEET  │   │   MOBILE     │   │  INSURANCE   │        │
    │   │     API      │   │     APP      │   │     API      │        │
    │   │              │   │              │   │              │        │
    │   │ Powerwall    │   │  iOS/Android │   │ Risk Score   │        │
    │   │ Coordination │   │  Dashboard   │   │ Data Feed    │        │
    │   └──────────────┘   └──────────────┘   └──────────────┘        │
    │                                                                  │
    └──────────────────────────────────────────────────────────────────┘
```

---

# 2. DEVICE SPECIFICATIONS

## DEVICE 1: ALEXANDER HUB 1.1 (HIGH COMPLEXITY)

### Purpose
Central brain - displays status, runs AI, coordinates all sensors, communicates with Tesla API.

### Processor

| Component | Part Number | Source | Notes |
|-----------|-------------|--------|-------|
| Compute Module | Raspberry Pi CM4104032 | RPi Foundation | 4GB RAM, 32GB eMMC, WiFi |
| Carrier Board | CUSTOM | **BUILD** | Needs design |

### Wireless Radios

| Protocol | Chip | Part Number | Source | Notes |
|----------|------|-------------|--------|-------|
| Zigbee 3.0 | CC2652P7 | CC2652P7RGZ | TI/DigiKey | Coordinator, +20dBm |
| WiFi 6 + BLE | ESP32-S3 | ESP32-S3-WROOM-1 | Espressif | Cloud connectivity |
| LoRa 915MHz | SX1262 | E22-900M30S | Ebyte | Foundation sensors |
| LTE Cat-M1 | BG96 | BG96MA-128-SGN | Quectel | Cellular backup |

### Display

| Component | Part Number | Source | Notes |
|-----------|-------------|--------|-------|
| 7" IPS LCD | WaveShare 7inch HDMI LCD | WaveShare | 1024x600, IPS |
| Touch Controller | GT911 | Goodix | I2C capacitive |

### Sensors (Built into Hub)

| Sensor | Model | Measures | Interface | Source |
|--------|-------|----------|-----------|--------|
| PM2.5/PM10 | Sensirion SPS30 | PM1.0, PM2.5, PM10 | I2C/UART | DigiKey |
| CO2 | Sensirion SCD41 | 400-5000 ppm | I2C | DigiKey |
| VOC/NOx | Sensirion SGP41 | VOC Index | I2C | DigiKey |
| Temp/Humidity | Sensirion SHT45 | Temp, RH | I2C | DigiKey |
| Barometric | Bosch BMP390 | Pressure | I2C | DigiKey |
| CO | Figaro TGS5042 | 0-1000 ppm | Analog | DigiKey |
| Methane | Winsen MQ-4 | Natural gas | Analog | Amazon/AliExpress |
| Smoke | Photoelectric | Smoke particles | Analog | Various |

### Power

| Component | Specification | Notes |
|-----------|---------------|-------|
| Input | 12V DC, 3A | Via PoE or wall adapter |
| Battery | 3x Samsung INR18650-35E | 10,500mAh total |
| Backup Time | 8+ hours | Normal operation |
| Charger IC | TI BQ25895 | Smart charging |
| Fuel Gauge | Maxim MAX17048 | Battery % |

### Firmware Stack

| Layer | Technology | Notes |
|-------|------------|-------|
| OS | Yocto Linux | Custom build, fast boot |
| UI Framework | Qt5 or Flutter | Touch interface |
| AI Runtime | TensorFlow Lite | Edge inference |
| ML Models | XGBoost | Predictive algorithms |
| Zigbee Stack | Z-Stack 3.0 | TI's stack on CC2652 |
| MQTT | Mosquitto | Local message broker |

---

## DEVICE 2: WATER GUARDIAN (MEDIUM COMPLEXITY)

### Purpose
Main water shutoff valve with flow/pressure/quality monitoring.

### Core Components

| Component | Part Number | Source | Notes |
|-----------|-------------|--------|-------|
| Motorized Ball Valve | US Solid 3/4" NPT | Amazon/US Solid | 12V, <3 sec close |
| MCU | ESP32-C6-WROOM-1 | Espressif | WiFi 6 + BLE |
| Zigbee | CC2652P7 (via SPI) | TI | Or use Zigbee module |
| Motor Driver | TI DRV8876 | DigiKey | H-bridge for valve |

### Sensors

| Sensor | Model | Measures | Notes |
|--------|-------|----------|-------|
| Ultrasonic Flow | TUF-2000M style | 0.1-25 GPM | Clamp-on, non-invasive |
| Pressure | Honeywell MIPAN2XX200PSA | 0-200 PSI | Stainless, 1/4" NPT |
| TDS | DFRobot DFR0300 | Total dissolved solids | Inline probe |
| Turbidity | DFRobot SEN0189 | Water clarity | LED-based |
| Temperature | DS18B20 | Pipe temp | Waterproof |

### Power

| Component | Specification | Notes |
|-----------|---------------|-------|
| Primary | 24V AC (from HVAC transformer) | Common in homes |
| Battery | LiFePO4 12V 3Ah | 8+ hour backup |
| Charger | TI BQ24618 | LiFePO4 compatible |

---

## DEVICE 3: HVAC SENTINEL (MEDIUM COMPLEXITY)

### Purpose
Filter life monitoring via differential pressure + UV-C pathogen control.

### Core Components

| Component | Part Number | Source | Notes |
|-----------|-------------|--------|-------|
| MCU | ESP32-C6-WROOM-1 | Espressif | |
| Diff Pressure Sensor | Freescale MPXV7002DP | DigiKey | 0-500 Pa |
| UV-C Lamp | GPH436T5L (18W) x2 | LSE Lighting | 253.7nm germicidal |
| UV Ballast | Generic 36W ballast | Amazon | Powers 2x 18W lamps |
| Current Sensor | SCT-013-030 | Amazon | HVAC blower monitoring |

### Operation Logic

```
IF hvac_blower = ON:
    uvc_lamp = ON
    read differential_pressure
    calculate filter_life_percent

IF filter_life_percent > 75%:
    send_alert("Replace filter soon")

IF filter_life_percent > 90%:
    send_alert("Replace filter NOW")
```

---

## DEVICE 4: AIR SENSOR (LOW COMPLEXITY)

### Purpose
Room-level air quality monitoring with e-ink display.

### Core Components

| Component | Part Number | Source | Notes |
|-----------|-------------|--------|-------|
| MCU | ESP32-C6-MINI-1 | Espressif | Small form factor |
| PM Sensor | Plantower PMS5003 | AliExpress | PM1, PM2.5, PM10 |
| CO2 | Sensirion SCD41 | DigiKey | |
| VOC | Sensirion SGP41 | DigiKey | |
| Temp/Humidity | Sensirion SHT45 | DigiKey | |
| Display | 2.9" E-ink | Good Display | Always-on, low power |

### Power
- USB-C (5V) primary
- 2x AA lithium backup (6 month life in low-power mode)

---

## DEVICE 5: FOUNDATION SENSOR (LOW COMPLEXITY)

### Purpose
Structural health monitoring - detects foundation settling before cracks appear.

### Core Components

| Component | Part Number | Source | Notes |
|-----------|-------------|--------|-------|
| MCU | ESP32-S3-MINI-1 | Espressif | |
| LoRa Module | Ebyte E22-900M30S | AliExpress | 1km range through concrete |
| Accelerometer | ST LIS2DH12 | DigiKey | 0.001 degree resolution |
| Vibration | Analog Devices ADXL345 | DigiKey | |
| Temp/Humidity | Sensirion SHT45 | DigiKey | |

### Power
- 2x D-cell lithium (5-7 year life)
- LoRa is extremely low power (~10 transmissions/day)

---

## DEVICE 6: GAS GUARDIAN (LOW COMPLEXITY)

### Purpose
Multi-gas detection with 85dB local alarm.

### Core Components

| Component | Part Number | Source | Notes |
|-----------|-------------|--------|-------|
| MCU | ESP32-C6-MINI-1 | Espressif | |
| Methane | Winsen MQ-4 | Amazon | Requires heater power |
| CO | Winsen MQ-7 | Amazon | Requires heater power |
| Piezo Buzzer | Generic 85dB | Amazon | Local alarm |

### Power
- AC powered (120V via USB adapter) - gas sensors need heater

---

## DEVICE 7: LEAK SPOT (LOW COMPLEXITY)

### Purpose
Point water detection sensor for under sinks, near water heater, etc.

### Core Components

| Component | Part Number | Source | Notes |
|-----------|-------------|--------|-------|
| MCU | ESP32-C6-MINI-1 | Espressif | |
| Water Sense Cable | Conductive rope 6ft | Amazon | Any point triggers |
| Temp/Humidity | Sensirion SHT45 | DigiKey | Freeze warning |

### Power
- 2x AA lithium (3-5 year life)
- Sleep mode, wake on water detection

---

# 3. BUILD vs BUY MATRIX

## WE BUY (Off-the-Shelf)

| Category | Components | Supplier |
|----------|------------|----------|
| **Processors** | Raspberry Pi CM4, ESP32-C6/S3 | RPi Foundation, Espressif |
| **Sensors** | All Sensirion, Plantower, Bosch, Figaro | DigiKey, Mouser |
| **Radios** | CC2652P7, SX1262, BG96 | TI, Semtech, Quectel |
| **Display** | 7" LCD, E-ink modules | WaveShare, Good Display |
| **Valve** | Motorized ball valve 3/4" | US Solid |
| **Power ICs** | BQ25895, MAX17048, regulators | TI, Maxim |
| **Batteries** | 18650 cells, LiFePO4, lithium AA/D | Samsung, various |
| **Passive components** | Resistors, capacitors, connectors | DigiKey |

## WE BUILD (Custom)

| Category | What We Create | Complexity |
|----------|----------------|------------|
| **Hub Carrier Board** | PCB connecting CM4 to radios, sensors, display | HIGH |
| **Sensor Node PCBs** | Custom boards for each sensor device | MEDIUM |
| **Firmware** | ESP-IDF code for all ESP32 devices | HIGH |
| **Hub Software** | Linux apps, UI, MQTT broker, AI models | HIGH |
| **Mobile App** | iOS + Android (React Native or Flutter) | MEDIUM |
| **Cloud Backend** | AWS IoT, database, API gateway | MEDIUM |
| **Enclosures** | Industrial design, injection molds | MEDIUM (outsource design) |
| **Zigbee Network** | Mesh configuration, coordinator firmware | MEDIUM |

---

# 4. COMMUNICATION PROTOCOLS

## Protocol Selection

| Protocol | Use Case | Range | Power | Data Rate |
|----------|----------|-------|-------|-----------|
| **Zigbee 3.0** | Most sensors to Hub | 100m indoor | Low | 250 kbps |
| **LoRa 915MHz** | Foundation sensor (through concrete) | 1+ km | Very Low | 0.3-50 kbps |
| **WiFi 6** | Hub to cloud | Standard | High | 100+ Mbps |
| **LTE Cat-M1** | Cellular backup | Nationwide | Medium | 1 Mbps |
| **BLE 5.2** | Phone setup, beacons | 50m | Low | 2 Mbps |

## Zigbee Network Topology

```
                    ┌──────────────┐
                    │  HUB         │
                    │ (Coordinator)│
                    │  CC2652P7    │
                    └──────┬───────┘
                           │
           ┌───────────────┼───────────────┐
           │               │               │
    ┌──────▼──────┐ ┌──────▼──────┐ ┌──────▼──────┐
    │ WATER       │ │    GAS      │ │   HVAC      │
    │ GUARDIAN    │ │  GUARDIAN   │ │  SENTINEL   │
    │ (Router)    │ │ (End Device)│ │ (Router)    │
    └──────┬──────┘ └─────────────┘ └──────┬──────┘
           │                               │
    ┌──────▼──────┐                 ┌──────▼──────┐
    │ LEAK SPOT 1 │                 │ AIR SENSOR  │
    │ (End Device)│                 │ (End Device)│
    └─────────────┘                 └─────────────┘
```

## Message Format (Example)

```json
{
  "device_id": "leak_spot_001",
  "device_type": "leak_spot",
  "timestamp": 1703123456,
  "readings": {
    "water_detected": true,
    "temperature_c": 18.5,
    "humidity_pct": 65,
    "battery_pct": 87
  },
  "alert_level": "critical"
}
```

---

# 5. FIRMWARE REQUIREMENTS

## ESP32 Firmware (All Sensor Nodes)

| Requirement | Implementation |
|-------------|----------------|
| Framework | ESP-IDF v5.x (FreeRTOS based) |
| Zigbee Stack | ESP-Zigbee (Espressif's implementation) |
| OTA Updates | ESP-IDF OTA partition scheme |
| Deep Sleep | <10uA sleep current for battery devices |
| Watchdog | Hardware WDT, auto-reset on hang |
| Secure Boot | Optional but recommended |

## Hub Firmware/Software

| Component | Technology |
|-----------|------------|
| OS | Yocto Linux (custom layer) |
| Init System | systemd |
| UI | Qt5 with QML or Flutter Linux |
| Zigbee Coordinator | zigbee2mqtt or custom Z-Stack app |
| LoRa Handler | Custom Python/C daemon |
| MQTT Broker | Mosquitto |
| AI Inference | TensorFlow Lite + Python |
| Cloud Sync | MQTT to AWS IoT Core |
| Tesla API | Python requests library |

## Key Firmware Features Needed

1. **Sensor fusion** - Combine multiple sensor readings
2. **Local decision making** - Act without cloud
3. **Emergency response sequence** - Sub-3-second valve close
4. **OTA updates** - Update all devices remotely
5. **Mesh self-healing** - Zigbee mesh repairs itself
6. **Battery management** - Accurate fuel gauge, low-power modes
7. **Fail-safe defaults** - If hub dies, valve stays in last state

---

# 6. POWER ARCHITECTURE

## Hub Power

```
           ┌─────────────────────────────────────────────────┐
           │                                                 │
  12V DC ──┼──► [BQ25895 Charger] ──► [3x 18650 Battery]    │
  (PoE or  │           │                     │               │
  adapter) │           ▼                     ▼               │
           │    [Fuel Gauge MAX17048]        │               │
           │           │                     │               │
           │           ▼                     ▼               │
           │    ┌──────────────────────────────┐             │
           │    │      POWER DISTRIBUTION      │             │
           │    ├──────────────────────────────┤             │
           │    │ 5V  → RPi CM4, Display       │             │
           │    │ 3.3V → Sensors, Radios       │             │
           │    │ 12V → Fan, Audio Amp         │             │
           │    └──────────────────────────────┘             │
           │                                                 │
           └─────────────────────────────────────────────────┘
```

## Water Guardian Power

```
  24V AC ──► [Rectifier] ──► [BQ24618] ──► [LiFePO4 12V]
  (HVAC)                          │              │
                                  ▼              ▼
                           [Power MUX] ──► [Valve Motor 12V]
                                  │
                                  ▼
                           [DC-DC 3.3V] ──► [ESP32, Sensors]
```

---

# 7. BILL OF MATERIALS (Summary)

## Per-Device Manufacturing Cost

| Device | BOM | Assembly | Total | Retail | Margin |
|--------|-----|----------|-------|--------|--------|
| Hub 1.1 | $410 | $40 | $450 | $799 | 44% |
| Water Guardian | $232 | $32 | $264 | $699 | 62% |
| HVAC Sentinel | $135 | $20 | $155 | $399 | 61% |
| Air Sensor | $48 | $8 | $56 | $169 | 67% |
| Foundation | $46 | $8 | $54 | $199 | 73% |
| Gas Guardian | $32 | $6 | $38 | $149 | 74% |
| Leak Spot | $18 | $4 | $22 | $69 | 68% |

## Prototype Development Budget

| Item | Qty | Unit Cost | Total |
|------|-----|-----------|-------|
| ESP32-C6 DevKit | 10 | $10 | $100 |
| ESP32-S3 DevKit | 5 | $15 | $75 |
| Raspberry Pi 4 (for dev) | 2 | $75 | $150 |
| CC2652P7 LaunchPad | 2 | $40 | $80 |
| SX1262 LoRa modules | 4 | $15 | $60 |
| Sensirion sensor kit | 1 | $150 | $150 |
| Plantower PMS5003 | 3 | $15 | $45 |
| MQ-series gas sensors | 5 | $5 | $25 |
| Motorized valve | 1 | $50 | $50 |
| Misc (wires, breadboards, etc) | - | - | $100 |
| **TOTAL PROTOTYPE BUDGET** | | | **~$835** |

---

# 8. DEVELOPMENT PHASES

## Phase 1: Proof of Concept (4-6 weeks)

**Goal:** Prove the core system works

| Task | Hardware | Firmware |
|------|----------|----------|
| Leak Spot → Hub | ESP32 dev board + water sensor | Basic Zigbee join, send alert |
| Hub display | RPi 4 + 7" display | Show alert on screen |
| Valve control | Valve + relay | Close on command |
| Demo sequence | - | Leak → Alert → Valve close |

**Deliverable:** Working demo of core water protection

---

## Phase 2: Full Prototype (8-12 weeks)

**Goal:** All 7 devices working together

| Task | Details |
|------|---------|
| Hub carrier board | Design PCB for CM4 + all radios |
| Sensor node PCBs | Simple boards for each sensor type |
| Zigbee mesh | Multi-hop, self-healing |
| LoRa foundation | Long-range basement sensor |
| Tesla API | OAuth, Powerwall commands |
| Basic mobile app | View sensors, receive alerts |

**Deliverable:** 10 prototype kits for testing

---

## Phase 3: Pilot Program (8-12 weeks)

**Goal:** Real-world testing in 25 homes

| Task | Details |
|------|---------|
| Enclosure design | Industrial design, tooling |
| Small production run | 50-100 units |
| Installation in homes | Real-world data collection |
| Bug fixes | Firmware updates OTA |
| Certification prep | Pre-compliance testing |

**Deliverable:** Validated product ready for certification

---

## Phase 4: Production (12-16 weeks)

**Goal:** Certified product ready for sale

| Task | Details |
|------|---------|
| UL certification | Safety (UL 60730, UL 1998) |
| FCC certification | RF emissions (Part 15) |
| Manufacturing handoff | Contract manufacturer setup |
| Production run | 1000+ units |

---

# 9. OPEN QUESTIONS FOR DISCUSSION

These are decisions we need to make together:

## Hardware Questions

1. **Zigbee approach:** Use ESP32-C6 with external CC2652? Or ESP32-H2 (has built-in Zigbee)?
2. **Hub display:** Qt5 (more mature) or Flutter (cross-platform with mobile)?
3. **PCB manufacturing:** US (faster, expensive) or China (slower, cheaper)?
4. **Enclosure:** Off-the-shelf enclosures or custom injection molded?

## Firmware Questions

5. **Zigbee stack:** ESP-Zigbee, Z-Stack, or zigbee2mqtt?
6. **Hub OS:** Full Yocto build or start with Raspberry Pi OS + harden later?
7. **OTA strategy:** How to update ESP32s in the field?
8. **Fail-safe behavior:** What should each device do if it loses hub connection?

## Architecture Questions

9. **Cloud backend:** AWS IoT Core, Azure IoT, or self-hosted?
10. **Mobile app:** Native (separate iOS/Android) or cross-platform (Flutter/React Native)?
11. **Tesla API auth:** How to handle OAuth tokens securely on Hub?

---

# APPENDIX A: KEY COMPONENT DATASHEETS

| Component | Datasheet URL |
|-----------|---------------|
| ESP32-C6 | https://www.espressif.com/en/products/socs/esp32-c6 |
| CC2652P7 | https://www.ti.com/product/CC2652P7 |
| RPi CM4 | https://www.raspberrypi.com/products/compute-module-4 |
| SPS30 | https://sensirion.com/products/catalog/SPS30 |
| SCD41 | https://sensirion.com/products/catalog/SCD41 |
| BQ25895 | https://www.ti.com/product/BQ25895 |
| SX1262 | https://www.semtech.com/products/wireless-rf/lora-connect/sx1262 |

---

# APPENDIX B: SUPPLIER CONTACTS

| Supplier | What They Sell | Website |
|----------|----------------|---------|
| DigiKey | Sensors, ICs, connectors | digikey.com |
| Mouser | Same as DigiKey | mouser.com |
| Espressif | ESP32 modules | espressif.com |
| Adafruit | Dev boards, breakouts | adafruit.com |
| SparkFun | Dev boards, tutorials | sparkfun.com |
| LCSC | Cheap components (China) | lcsc.com |
| JLCPCB | PCB manufacturing | jlcpcb.com |
| PCBWay | PCB + assembly | pcbway.com |
| Seeed Studio | PCB + small batch assembly | seeedstudio.com |

---

**Document prepared by:** Eric Deloera
**For:** Joe Hobart, Firmware Engineer
**Contact:** 405-590-2060

**Next step:** Schedule call to discuss Phase 1 approach and answer open questions.
