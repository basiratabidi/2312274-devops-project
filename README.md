# 2312274 — DevOps Final Project

> **Student:** Basirat Zehra — 2312274
> **Course:** DevOps Fundamentals — SZABIST
> **Instructor:** Afaq Ahmed
> **Live URL:** http://54.227.74.215:8000

## Architecture
GitHub Push

│

├── CI Pipeline (GitHub Actions)

│       ├── flake8 lint

│       └── pytest (PostgreSQL service container)

│

└── CD Pipeline — runs only after CI passes

└── SSH into EC2

└── git pull + docker compose up --build
**Services:**
- `web` — FastAPI + Uvicorn on port 8000
- `db`  — PostgreSQL 15 with persistent named volume

## Local Setup

```bash
git clone https://github.com/basiratabidi/2312274-devops-project
cd 2312274-devops-project
cp .env.example .env
docker compose up --build
curl http://localhost:8000/health
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /health | Health check + DB status |
| POST | /students | Create student record |
| GET | /students | List all students |
| GET | /students/{reg_no} | Get student by reg no |
| DELETE | /students/{reg_no} | Delete student |

## Running Tests

```bash
python3.12 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
DATABASE_URL=sqlite:///./test.db pytest app/tests/ -v
```

## GitHub Secrets needed
- `EC2_HOST` — EC2 public IP
- `EC2_SSH_KEY` — contents of .pem private key
