# Inventory Management System (IMS)

A real-time inventory management system built with a FastAPI 
backend and Streamlit frontend. Designed as a single internal 
dashboard for managing product inventory including full CRUD 
operations, stock management, and real-time metrics.

---
## Prerequisites

- Python 3.12
- uv
- MongoDB (local or Atlas)
- Docker (optional, for SonarQube)

---

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com//inventory-management-system-IMS.git
cd inventory-management-system-IMS
```

### 2. Install uv

**Linux / macOS:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Windows (PowerShell):**
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### 3. Install Dependencies

```bash
uv sync
```

### 4. Configure Environment Variables

Copy the example env file and fill in your values:

```bash
cp .env.example .env
```
Open `.env` and set:
MONGODB_URL=your_mongodb_connection_string

DATABASE_NAME=IMS

BACKEND_URL=http://localhost:8000

SONAR_HOST_URL=http://localhost:9000

SONAR_TOKEN=your_sonar_token
### 5. Install Pre-commit Hooks

```bash
uv run pre-commit install
```

---

## Running the Application

### Backend

```bash
uv run uvicorn backend.main:app --reload
```

Backend runs at `http://localhost:8000`
API docs available at `http://localhost:8000/redoc`

### Frontend

```bash
uv run streamlit run frontend/dashboard.py
```

Frontend runs at `http://localhost:8501`

---

## Running Both Together

Open two terminal windows:

**Terminal 1 — Backend:**
```bash
uv run uvicorn backend.main:app --reload
```

**Terminal 2 — Frontend:**
```bash
uv run streamlit run frontend/dashboard.py
```

---

## Code Quality

**Run linter:**
```bash
uv run ruff check .
```

**Run type checker:**
```bash
uv run mypy .
```

**Run pre-commit hooks:**
```bash
uv run pre-commit run --all-files
```

---

## MongoDB (Local)

Start MongoDB via Docker

```bash
docker run -d --name mongodb -p 27017:27017 mongo:latest
```

Add to your `.env`:
MONGODB_URL=mongodb://localhost:27017

## SonarQube (Local)

Start SonarQube via Docker:

```bash
docker run -d --name sonarqube -p 9000:9000 sonarqube:community
```

Run the scanner:

```bash
uv run pysonar
```

Dashboard available at `http://localhost:9000`

---

## Project Structure

```
inventory-management-system-IMS/
├── backend/
│   ├── api/
│   │   └── routes/
│   │       ├── metrics.py
│   │       └── products.py
│   ├── core/
│   │   ├── config.py
│   │   └── database.py
│   ├── models/
│   │   └── products.py
│   ├── schemas/
│   │   ├── metrics.py
│   │   └── products.py
│   ├── utils/
│   │   └── sku.py
│   └── main.py
├── frontend/
│   ├── client.py
│   └── dashboard.py
├── .github/
│   ├── workflows/
│   │   └── code-quality.yml
│   └── pull_request_template.md
├── .env.example
├── .pre-commit-config.yaml
├── pyproject.toml
└── uv.lock
```

## Features

- **Create** products with auto-generated SKU
- **Read** all products in a clean dashboard layout
- **Update** product details inline
- **Delete** products with confirmation
- **Restock** inventory with a single click (+10 units)
- **Search** products by name or SKU
- **Filter** products by category
- **Real-time metrics** — total products, asset valuation, out of stock count

---

## Environment Variables

| Variable | Description | Default |
|---|---|---|
| `MONGODB_URL` | MongoDB connection string | — |
| `DATABASE_NAME` | MongoDB database name | `IMS` |
| `BACKEND_URL` | FastAPI backend URL | `http://localhost:8000` |
| `SONAR_HOST_URL` | SonarQube server URL | `http://localhost:9000` |
| `SONAR_TOKEN` | SonarQube authentication token | — |
