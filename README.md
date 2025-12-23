# ALEXANDER one.1

**Multi-Peril Smart Home Protection System**

By PergoLuxx Construction LLC

---

## Overview

ALEXANDER one.1 is a comprehensive smart home protection platform that prevents costly insurance claims through automatic detection and shutoff of:

- **Water leaks** - Automatic main shutoff prevents flooding
- **Gas leaks** - Methane, propane, and CO detection with valve control
- **Fire/Smoke** - Early detection and alert system
- **Stove safety** - Automatic gas shutoff when cooking is unattended (unique to ALEXANDER)

### Why ALEXANDER?

| Feature | Flo | Ting | LeakBot | ALEXANDER |
|---------|-----|------|---------|-----------|
| Water shutoff | Yes | No | No | Yes |
| Gas detection | No | No | No | Yes |
| Electrical monitoring | No | Yes | No | Planned |
| Stove safety | No | No | No | **Yes** |
| Unified platform | No | No | No | **Yes** |

---

## Project Structure

```
alexander-one1/
├── backend/           # Go API server
│   ├── cmd/          # Entry points
│   ├── internal/     # Core services
│   └── pkg/          # Shared packages
├── sensors/          # Python sensor drivers
│   ├── core/         # Config, database, events
│   ├── sensors/      # Sensor implementations
│   ├── controllers/  # Valve controllers
│   └── api/          # REST API
├── docs/             # Documentation
├── hardware/         # Wiring diagrams, specs
├── scripts/          # Build and utility scripts
├── legal/            # Warranty, liability, ToS
└── pdfs/             # Generated documents
```

---

## Quick Start

### Requirements

- Raspberry Pi 4 (4GB+ recommended)
- Python 3.9+
- Go 1.20+
- Docker (optional)

### Installation

```bash
# Clone repository
git clone https://github.com/ricocyber/alexander-one1.git
cd alexander-one1

# Python sensors
cd sensors
pip install -r requirements.txt
python -m src.main --simulation

# Go backend
cd ../backend
go run cmd/api/main.go
```

### Simulation Mode

For testing without hardware:

```bash
export LUXX_HAUS_SIMULATION=true
python -m src.main
```

---

## Hardware

### Supported Sensors

| Sensor | Model | Interface |
|--------|-------|-----------|
| Water Pressure | Honeywell PX2 | Analog (ADC) |
| Gas (Methane) | MQ-4 | Analog (ADC) |
| Gas (Propane) | MQ-6 | Analog (ADC) |
| CO | MQ-7 | Analog (ADC) |
| Smoke | MQ-2 | Analog (ADC) |
| Temperature | DHT22/SHT31 | Digital (GPIO/I2C) |
| Motion (PIR) | HC-SR501 | Digital (GPIO) |
| Stove Heat | MLX90614 | I2C |

### Supported Valves

| Valve | Type | Interface |
|-------|------|-----------|
| Water Shutoff | Motorized ball valve | GPIO relay |
| Gas Shutoff | NC solenoid (CSA certified) | GPIO relay |

See `hardware/wiring-diagram.md` for detailed connections.

---

## Documentation

| Document | Description |
|----------|-------------|
| [Installation Guide](docs/INSTALLATION_GUIDE.md) | Complete setup instructions |
| [Hardware Specs](pdfs/IHP_Hardware_Technical_Spec.pdf) | Technical specifications |
| [Market Research](docs/IHP_Market_Research_Data.md) | $27B market opportunity |
| [Warranty](legal/WARRANTY.md) | 2-year limited warranty |
| [Liability Disclaimer](legal/LIABILITY_DISCLAIMER.md) | Important safety info |
| [Terms of Service](legal/TERMS_OF_SERVICE.md) | Usage terms |

---

## Unique Features

### Stove Safety System

ALEXANDER's differentiator - no competitor has this:

```
Stove ON + No Motion for 3 min = WARNING notification
Stove ON + No Motion for 5 min = AUTOMATIC GAS SHUTOFF
```

33% of home fires are caused by unattended cooking. ALEXANDER prevents them.

### Multi-Peril Platform

Instead of buying 4 different devices:
- Flo for water ($500)
- Ting for electrical ($150)
- Nest Protect for smoke ($119)
- Plus gas monitoring

ALEXANDER provides unified protection in one platform.

---

## Insurance Partnership

ALEXANDER is designed for insurance carrier partnerships:

- **96% claim reduction** proven for water damage (Flo data)
- **80% reduction** in electrical fires (Ting data)
- **Proactive loss prevention** vs reactive claims processing
- **API integration** for automated risk scoring

Contact: partnerships@luxxhaus.com

---

## Regulatory Compliance

- FCC Part 15 Class B (pending)
- UL Listed (pending)
- CSA Certified gas components
- Designed for NFPA 72 compliance

---

## License

Proprietary - All Rights Reserved
Patent Pending

---

## Contact

**PergoLuxx Construction LLC**

- Website: www.luxxhaus.com
- Email: info@luxxhaus.com
- Support: support@luxxhaus.com
- Phone: 1-800-XXX-XXXX

---

*ALEXANDER one.1 - Preventing the $28 Billion in Annual Home Insurance Claims*
