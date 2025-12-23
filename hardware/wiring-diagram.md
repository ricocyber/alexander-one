# LUXX HAUS Hardware Wiring Guide

## Overview

This guide covers the hardware setup for the LUXX HAUS smart home protection system using a Raspberry Pi 4.

## Required Components

### Main Controller
- Raspberry Pi 4 (4GB+ recommended)
- 32GB+ microSD card
- 5V 3A USB-C power supply
- Official Raspberry Pi case (or custom enclosure)

### Sensors

| Sensor | Model | Purpose | Quantity |
|--------|-------|---------|----------|
| Water Pressure | Honeywell PX2 | Leak detection | 1 |
| Gas (Methane) | MQ-4 | Natural gas detection | 1-2 |
| Gas (CO) | MQ-7 | Carbon monoxide detection | 1-2 |
| Smoke | MQ-2 | Fire detection | 2-4 |
| Temperature | DHT22 | Freeze prevention | 2-4 |

### Valves

| Valve | Model | Purpose |
|-------|-------|---------|
| Water Main | US Solid 1" Motorized Ball Valve | Water shutoff |
| Gas Line | Emerson ASCO Gas Solenoid | Gas shutoff |

### Supporting Components
- MCP3008 ADC (for analog sensors)
- 4-channel relay module (5V)
- 12V/24V power supply (for valves)
- Level shifter (3.3V to 5V)
- Terminal blocks
- Enclosure (IP65 for outdoor sensors)

## Wiring Diagram

```
                     RASPBERRY PI 4 GPIO
                    ┌─────────────────────┐
                    │  3V3  (1)  (2) 5V   │
                    │  SDA  (3)  (4) 5V   │
                    │  SCL  (5)  (6) GND  │
           DHT22 ◄──│  GP4  (7)  (8) TXD  │
                    │  GND  (9) (10) RXD  │
                    │  GP17(11) (12) GP18 │──► Water Valve Relay
    Water Valve ◄───│  GP27(13) (14) GND  │
      Gas Valve ◄───│  GP22(15) (16) GP23 │
                    │  3V3 (17) (18) GP24 │
         MOSI ◄─────│  GP10(19) (20) GND  │
         MISO ◄─────│  GP9 (21) (22) GP25 │
         SCLK ◄─────│  GP11(23) (24) GP8  │──► ADC CS
                    │  GND (25) (26) GP7  │
                    │  ID_SD(27)(28)ID_SC │
                    │  GP5 (29) (30) GND  │
                    │  GP6 (31) (32) GP12 │
                    │  GP13(33) (34) GND  │
                    │  GP19(35) (36) GP16 │
                    │  GP26(37) (38) GP20 │
                    │  GND (39) (40) GP21 │
                    └─────────────────────┘
```

## MCP3008 ADC Wiring

The MCP3008 converts analog sensor signals to digital for the Raspberry Pi.

```
         MCP3008
        ┌───────┐
CH0 ◄───│1    16│───► VDD (3.3V)
CH1 ◄───│2    15│───► VREF (3.3V)
CH2 ◄───│3    14│───► AGND
CH3 ◄───│4    13│───► CLK (SCLK - GPIO 11)
CH4 ◄───│5    12│───► DOUT (MISO - GPIO 9)
CH5 ◄───│6    11│───► DIN (MOSI - GPIO 10)
CH6 ◄───│7    10│───► CS (GPIO 8)
CH7 ◄───│8     9│───► DGND
        └───────┘

Channel Assignments:
- CH0: Water Pressure Sensor
- CH1: MQ-4 Gas Sensor
- CH2: MQ-2 Smoke Sensor
- CH3: MQ-7 CO Sensor
- CH4-7: Available for expansion
```

## Sensor Connections

### Water Pressure Sensor (Honeywell PX2)

```
PX2 Sensor          MCP3008
┌─────────┐        ┌───────┐
│ VCC (Red)│───────│ 5V    │
│ GND (Blk)│───────│ GND   │
│ OUT (Yel)│───────│ CH0   │
└─────────┘        └───────┘

Note: PX2 outputs 0.5-4.5V. Use voltage divider if exceeding 3.3V.
```

### MQ-4 Gas Sensor

```
MQ-4 Module         MCP3008
┌─────────┐        ┌───────┐
│ VCC     │───────│ 5V    │
│ GND     │───────│ GND   │
│ AOUT    │───────│ CH1   │
│ DOUT    │ (unused for analog reading)
└─────────┘        └───────┘

Important: MQ sensors require 24-48 hour burn-in period.
```

### DHT22 Temperature/Humidity

```
DHT22              Raspberry Pi
┌─────────┐
│ VCC (1) │───────── 3.3V
│ DATA(2) │───────── GPIO 4 (with 10kΩ pull-up to 3.3V)
│ NC  (3) │ (not connected)
│ GND (4) │───────── GND
└─────────┘
```

## Relay Module Wiring

### 4-Channel Relay Module

```
Relay Module        Raspberry Pi
┌───────────┐
│ VCC       │───────── 5V
│ GND       │───────── GND
│ IN1       │───────── GPIO 17 (Water Valve Open)
│ IN2       │───────── GPIO 18 (Water Valve Close)
│ IN3       │───────── GPIO 27 (Gas Valve)
│ IN4       │───────── GPIO 22 (Spare)
└───────────┘

Note: Use optocoupler-isolated relay module for safety.
```

### Water Valve Connection

```
Relay 1 (Open)      Motorized Ball Valve
┌─────────┐        ┌─────────────────┐
│ COM     │────────│ Motor +         │
│ NO      │────────│ (via 12V supply)│
└─────────┘        └─────────────────┘

Relay 2 (Close)
┌─────────┐        
│ COM     │────────│ Motor -         │
│ NO      │────────│ (via 12V supply)│
└─────────┘        

Power: Separate 12V/24V supply for valve motor.
```

### Gas Valve Connection

```
Relay 3             Gas Solenoid
┌─────────┐        ┌─────────────┐
│ COM     │────────│ Valve +     │
│ NO      │────────│ (via 24V)   │
└─────────┘        │ Valve -     │───── 24V GND
                   └─────────────┘

CRITICAL: Gas valve must be CSA/UL certified for gas.
          Use normally-closed valve for fail-safe operation.
```

## Power Supply Setup

```
┌─────────────────────────────────────────┐
│            POWER DISTRIBUTION           │
├─────────────────────────────────────────┤
│                                         │
│  USB-C 5V 3A ──► Raspberry Pi           │
│                                         │
│  12V Supply ───► Water Valve Motor      │
│              └─► Relay Module VCC       │
│                                         │
│  24V Supply ───► Gas Solenoid Valve     │
│                                         │
│  5V Rail ──────► MQ Sensors (heaters)   │
│                                         │
│  3.3V Rail ────► ADC, DHT22             │
│                                         │
└─────────────────────────────────────────┘
```

## Safety Considerations

### Electrical Safety
1. Use proper gauge wire for valve currents
2. Include fuses on high-current circuits
3. Ground all metal enclosures
4. Use IP-rated enclosures for wet areas

### Gas Valve Safety
1. **Professional Installation Required** - Gas valves must be installed by licensed technician
2. Use only CSA/UL certified gas-rated valves
3. Normally-closed configuration is mandatory
4. Include manual bypass for emergencies

### Water Valve Safety
1. Install valve after main shutoff
2. Include manual override capability
3. Test monthly to prevent seizure

## Testing Procedure

### 1. Initial Power-On
```bash
# Check I2C devices
i2cdetect -y 1

# Check SPI
ls /dev/spidev*

# Test GPIO
pinctrl get 17  # Should show input/output state
```

### 2. Sensor Verification
```bash
# Run sensor test
python -m src.main --demo --demo-duration 60
```

### 3. Valve Testing
```bash
# Test via API
curl -X POST http://localhost:8000/api/v1/valves/water/close
curl -X POST http://localhost:8000/api/v1/valves/water/open
```

## Troubleshooting

### No ADC Readings
1. Check SPI is enabled: `sudo raspi-config`
2. Verify wiring to MCP3008
3. Check CS pin assignment

### DHT22 Errors
1. Check pull-up resistor (10kΩ to 3.3V)
2. Ensure single DHT22 per GPIO pin
3. Add retry logic (sensor is finicky)

### Valve Not Operating
1. Check relay LED indicators
2. Verify power supply voltage
3. Test relay coils with multimeter
4. Check GPIO pin configuration

## Enclosure Recommendations

### Indoor Controller Box
- Hammond 1591XXSFLBK (IP54)
- Include ventilation for Raspberry Pi
- DIN rail mount for clean installation

### Outdoor Sensor Housing
- Polycase WC-22F (IP65)
- Use cable glands for wire entry
- Include desiccant pack

## Pin Reference Summary

| GPIO | Function | Component |
|------|----------|-----------|
| 4 | DATA | DHT22 Temperature |
| 8 | SPI CS | MCP3008 ADC |
| 9 | SPI MISO | MCP3008 ADC |
| 10 | SPI MOSI | MCP3008 ADC |
| 11 | SPI SCLK | MCP3008 ADC |
| 17 | OUTPUT | Water Valve Open |
| 18 | OUTPUT | Water Valve Close |
| 27 | OUTPUT | Gas Valve |
| 22 | OUTPUT | Spare Relay |
