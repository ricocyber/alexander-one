# ALEXANDER ONE - ENGINEERING OVERVIEW

**Prepared for:** Joe Hobart | **Prepared by:** Eric Deloera | **Date:** December 2025

---

## WHAT IS ALEXANDER ONE?

Alexander One is a smart home protection platform - 7 devices that monitor water, air, gas, HVAC, and structural health. The system detects hazards and takes automated action to prevent damage.

**Key capability:** Integration with Tesla Powerwall via Fleet API. When a water leak is detected, the system commands Powerwall to prioritize the sump pump circuit while simultaneously closing the main water valve. Response time: under 3 seconds.

---

## THE 7 DEVICES

| Device | Function | Complexity |
|--------|----------|------------|
| **Alexander Hub** | Central processor - 7" touchscreen, multi-protocol radio, edge AI | High |
| **Water Guardian** | Main water shutoff valve + flow/pressure/quality monitoring | Medium |
| **HVAC Sentinel** | Filter monitoring + UV-C air treatment control | Medium |
| **Air Sensor** | Room air quality (PM2.5, CO2, VOC, temp, humidity) | Low |
| **Foundation Sensor** | Structural tilt detection (0.001° precision) via LoRa | Low |
| **Gas Guardian** | Methane + carbon monoxide detection with 85dB alarm | Low |
| **Leak Spot** | Battery-powered point water sensor with 6ft sensing cable | Low |

---

## HARDWARE ARCHITECTURE

### Hub (The Brain)

| Component | Part | Notes |
|-----------|------|-------|
| Processor | Raspberry Pi CM4 | 4GB RAM, 32GB eMMC |
| Zigbee Radio | TI CC2652P7 | Coordinator for all Zigbee devices |
| WiFi | ESP32-S3 | WiFi 6, cloud connectivity |
| LoRa | Semtech SX1262 | 915MHz, for foundation sensor (1km+ range) |
| LTE | Quectel BG96 | Cat-M1 cellular backup |
| Display | 7" capacitive touch | 1024x600 IPS |
| Battery Backup | 18650 cells | 6-8 hour runtime |
| AI/ML | TensorFlow Lite + XGBoost | Edge inference, no cloud required |

### Sensor Devices

| Device | MCU | Wireless | Power | Key Sensors |
|--------|-----|----------|-------|-------------|
| Water Guardian | ESP32-C6 | Zigbee 3.0 | 24V AC + 12V LiFePO4 backup | Ultrasonic flow, pressure transducer, TDS, turbidity |
| HVAC Sentinel | ESP32-C6 | Zigbee 3.0 | 24V HVAC tap | Differential pressure, UV-C control relay |
| Air Sensor | ESP32-C6 | Zigbee 3.0 | USB-C 5V | Sensirion SHT45, Bosch BME680, Plantower PMS5003, Sensirion SCD41 |
| Foundation | ESP32-C6 | LoRa 915MHz | 2x D-cell (5-7 year life) | STMicro LIS2DH12 (tilt), Analog Devices ADXL345 (vibration) |
| Gas Guardian | ESP32-C6 | Zigbee 3.0 | 120V AC plug | MQ-4 (methane), MQ-7 (CO), 85dB piezo buzzer |
| Leak Spot | ESP32-C6 | Zigbee 3.0 | 2x AA (3-5 year life) | Conductive water rope, SHT45 (temp/humidity) |

---

## COMMUNICATION FLOW

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│ Leak Spot   │     │ Gas Guardian│     │ Air Sensor  │
│ (Zigbee)    │     │ (Zigbee)    │     │ (Zigbee)    │
└──────┬──────┘     └──────┬──────┘     └──────┬──────┘
       │                   │                   │
       └───────────────────┼───────────────────┘
                           │
                    Zigbee 3.0 Mesh
                           │
                           ▼
                 ┌─────────────────┐
                 │  ALEXANDER HUB  │
                 │                 │
                 │  • CC2652P7     │◄──── LoRa ────── Foundation Sensor
                 │  • RPi CM4      │
                 │  • ESP32-S3     │
                 └────────┬────────┘
                          │
              ┌───────────┼───────────┐
              │           │           │
              ▼           ▼           ▼
        ┌─────────┐ ┌─────────┐ ┌─────────┐
        │  WiFi   │ │  Tesla  │ │  Cloud  │
        │ Router  │ │Powerwall│ │   API   │
        └─────────┘ └─────────┘ └─────────┘
```

---

## EMERGENCY RESPONSE SEQUENCE

**Example: Water leak detected**

1. **T+0ms** - Leak Spot detects water, sends Zigbee alert
2. **T+50ms** - Hub receives signal
3. **T+100ms** - AI confirms real leak (not false positive)
4. **T+150ms** - Hub checks for gas leak nearby (safety)
5. **T+300ms** - Hub sends parallel commands:
   - Tesla API: Keep sump pump circuit ON
   - Water Guardian: CLOSE valve
   - Cloud: Log event
6. **T+800ms** - Water valve fully closed
7. **T+1000ms** - Push notification to homeowner
8. **T+2000ms** - Insurance API logged

**Total response: <3 seconds**

---

## BUILD vs BUY

**Off-the-shelf (we buy):**
- All sensors (Sensirion, Plantower, Bosch, STMicro)
- Microcontrollers (ESP32-C6, CC2652P7)
- Raspberry Pi CM4
- Radio modules (SX1262, BG96)
- Motorized ball valve
- Display, batteries, power ICs

**Custom (we build):**
- PCB carrier boards for each device
- Firmware (C/C++ on ESP-IDF)
- Hub software (Python, Linux/Yocto)
- Communication protocol
- Prediction algorithms
- Tesla Fleet API integration
- Mobile app (iOS/Android)
- Cloud backend

---

## WIRELESS PROTOCOLS

| Protocol | Use Case | Range | Why |
|----------|----------|-------|-----|
| Zigbee 3.0 | Most sensors | 30-100m | Low power, mesh networking, proven |
| LoRa 915MHz | Foundation sensor | 1km+ | Penetrates concrete, basement-friendly |
| WiFi 6 | Hub to cloud | House | High bandwidth for updates |
| LTE Cat-M1 | Cellular backup | Anywhere | Works when WiFi/power down |

---

## POWER ARCHITECTURE

| Device | Primary | Backup | Runtime |
|--------|---------|--------|---------|
| Hub | 12V DC adapter | 18650 battery pack | 6-8 hours |
| Water Guardian | 24V AC (HVAC) | 12V LiFePO4 | 8+ hours valve operation |
| Gas Guardian | 120V AC plug | Supercapacitor | 10 min alarm |
| Foundation | 2x D-cell lithium | - | 5-7 years |
| Leak Spot | 2x AA lithium | - | 3-5 years |
| Air Sensor | USB-C 5V | - | Plug-in only |

---

## QUESTIONS THIS DOCUMENT MAY RAISE

| Question | Answer |
|----------|--------|
| Why ESP32-C6? | WiFi 6 + BLE + RISC-V, future-proof, low cost (~$3) |
| Why not ESP32 for Zigbee? | CC2652P7 is better Zigbee coordinator, ESP32 Zigbee support is newer/less stable |
| Why LoRa for foundation? | Needs to work through concrete basement walls, Zigbee won't reach |
| Why edge AI not cloud? | Critical decisions (shut off water) can't wait for cloud latency |
| Why Raspberry Pi CM4? | Proven, available, enough power for TensorFlow Lite, easy to develop |
| Certification requirements? | UL, FCC Part 15, potentially ETL for water valve |

---

## ATTACHMENTS

- **2_ENGINEERING_BLUEPRINT.md** - Full technical specifications
- **HARDWARE_SPECIFICATION.pdf** - Detailed component list and BOM

---

**Contact:** Eric Deloera | 405-590-2060 | luxx.okc@gmail.com

**CONFIDENTIAL - PATENT PENDING**
