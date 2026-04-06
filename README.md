![Python](https://img.shields.io/badge/python-3.10-blue)
![Status](https://img.shields.io/badge/status-in%20progress-yellow)

# Projeto-ESP32-DHT22

End-to-end IoT monitoring system built as a portfolio piece targeting firmware engineering roles. An ESP32 microcontroller reads temperature and humidity from a DHT22 sensor, transmits the data via MQTT, persists it in a local SQLite database, exposes it through a REST API, and displays it in an interactive dashboard.

---

## Overview

This project simulates a real-world IoT monitoring pipeline, focusing on:

- Real-time data ingestion using MQTT
- Decoupled system architecture
- Backend data persistence and querying
- API design for data consumption
- Data visualization

Designed to demonstrate skills relevant to firmware and backend engineering roles.

---

## Status

| Layer | Status |
|---|---|
| Database schema | ✅ Done |
| MQTT subscriber | ✅ Done |
| REST API | ✅ Done |
| Dashboard | ✅ Done |
| ESP32 firmware | ⏳ Next step |

---

## Architecture

```
ESP32 + DHT22
     │
     │  MQTT publish
     ▼
Mosquitto Broker
     │
     │  paho-mqtt subscribe
     ▼
Python Subscriber ──► SQLite (dht22.db)
                            │
                            │  SQLAlchemy ORM
                            ▼
                        FastAPI (REST API)
                            │
                            │  HTTP/JSON
                            ▼
                      Plotly Dash (Dashboard)
```

---

## Design Decisions

- MQTT was chosen for its lightweight publish/subscribe model, common in IoT systems
- SQLite used for simplicity and local development (can be replaced with PostgreSQL)
- FastAPI chosen for high performance and automatic documentation
- Decoupled subscriber to ensure scalability

---

## Tech Stack

| Layer | Technology |
|---|---|
| Microcontroller | ESP32 (PlatformIO + VSCode) |
| Sensor | DHT22 — temperature and humidity |
| Transport | MQTT (Mosquitto broker) |
| Subscriber | Python + paho-mqtt |
| Database | SQLite + SQLAlchemy ORM |
| API | FastAPI + Uvicorn |
| Dashboard | Plotly Dash |
| Version control | Git + GitHub (Conventional Commits) |
| OS | Linux |

---

## Project Structure

Current repository:

```
Projeto-ESP32-DHT22/
├── db/
│   ├── __init__.py
│   └── schema.py          # ReadDHT22 ORM model + SQLite setup
├── mqtt/
│   ├── __init__.py
│   └── subscriber.py      # MQTT subscriber + DB persistence
├── api/
│   ├── __init__.py
│   └── main.py            # FastAPI REST API
├── dash/
│   ├── dashboard.py       # Dash app entrypoint
│   ├── cards/
│   │   ├── average_temperature.py
│   │   └── most_readings_device.py
│   └── graphs/
│       └── temperature_over_time.py
├── simulator/
│   └── fake_esp32.py      # MQTT publisher to simulate ESP32 data
├── .env                   # Not versioned
├── .gitignore
├── requirements.txt
└── README.md
```

Planned next stage (firmware):

```
Projeto-ESP32-DHT22/
└── firmware/
     ├── src/
     │   └── main.cpp       # ESP32 firmware entrypoint
     └── platformio.ini
```

---

## API Endpoints

### `GET /sensor-readings`
Returns a paginated list of sensor readings with an optional device filter.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `limit` | int | 100 | Max number of records to return |
| `offset` | int | 0 | Number of records to skip |
| `device_id` | string | null | Filter by device ID |

**Examples:**
```
GET /sensor-readings
GET /sensor-readings?limit=10&offset=0
GET /sensor-readings?device_id=ESP32_001
```

---

### `GET /last-reading`
Returns the most recent sensor reading, optionally filtered by device.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `device_id` | string | null | Filter by device ID |

**Examples:**
```
GET /last-reading
GET /last-reading?device_id=ESP32_001
```

---

### `GET /average-reading`
Returns average temperature and humidity. By default, uses the last 30 days.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `device_id` | string | null | Filter by device ID |
| `intervalo1` | datetime (ISO 8601) | null | Start datetime filter |
| `intervalo2` | datetime (ISO 8601) | now | End datetime filter |

**Examples:**
```
GET /average-reading
GET /average-reading?device_id=ESP32_001
GET /average-reading?intervalo1=2026-04-01T00:00:00&intervalo2=2026-04-06T23:59:59
```

---

### `GET /most-readings-device`
Returns the device with the highest number of readings in the database.

**Example:**
```
GET /most-readings-device
```

---

## Data Model

```
leituras
├── id          INTEGER  PRIMARY KEY AUTOINCREMENT
├── temperature FLOAT    NOT NULL
├── humidity    FLOAT    NOT NULL
├── device_id   VARCHAR   DEFAULT "ESP32_01"
└── timestamp   DATETIME DEFAULT now()
```

---

## MQTT Payload

The ESP32 publishes to the topic `sensors/dht22` with the following JSON structure:

```json
{
  "temperature": 25.4,
  "humidity": 60.0,
  "device_id": "ESP32_01"
}
```

---

## How to Run

### Prerequisites

- Python 3.10+
- Mosquitto broker running locally
- Git

### Setup

```bash
# Clone the repository
git clone https://github.com/Terres06/Projeto-ESP32-DHT22.git
cd Projeto-ESP32-DHT22

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file manually and fill broker credentials
```

### Create the database

```bash
python -m db.schema
```

### Start the MQTT subscriber

```bash
python -m mqtt.subscriber
```

### Start the API

```bash
uvicorn api.main:app --reload
```

API docs available at: `http://127.0.0.1:8000/docs`

### Start the Dashboard

```bash
python dash/dashboard.py
```

Dashboard available at: `http://127.0.0.1:8050`

### Optional: Run ESP32 simulator publisher

Use this while firmware is still pending.

```bash
python simulator/fake_esp32.py
```

---

## Environment Variables

```
MQTT_BROKER=localhost
MQTT_PORT=1883
MQTT_USERNAME=
MQTT_PASSWORD=
MQTT_CLIENT_ID=python_subscriber
```

---

## Author

Pedro Terres — [github.com/Terres06](https://github.com/Terres06)
