# Incident & Response Simulator (CLI)

A small Python CLI tool that simulates how IT teams classify incidents, assign priority, and follow a response plan.
It logs incidents to a CSV file, supports incident IDs, and allows status updates (OPEN → IN_PROGRESS → CLOSED).

This project was built as part of my preparation for an IT Ausbildung in Germany.

---

## Features

- **Incident types**
  - Access Issue (login/permissions)
  - Network Failure (connectivity/VPN)
  - System Service Down (app/server stopped)
  - Phishing / Security Alert

- **Priority assignment**
  - Uses incident type + impact level + business blocked to assign:
    - LOW / MEDIUM / HIGH / CRITICAL

- **Response plan**
  - Prints a practical step-by-step response plan for each incident type

- **Incident logging**
  - Saves incidents into `incident_log.csv` with:
    - `id, time, incident, impact, business_blocked, priority, status`

- **Incident IDs**
  - Auto-generated numeric IDs like `INC-0001`, `INC-0002`, ...

- **Status updates**
  - Update incidents to:
    - OPEN / IN_PROGRESS / CLOSED

- **History viewer**
  - View all incidents
  - Filter HIGH + CRITICAL
  - Filter by incident type

---

## Tech Stack

- Python 3
- Standard library only (`csv`, `datetime`, `os`)

---

## How to Run

```bash
python incident_simulator.py
