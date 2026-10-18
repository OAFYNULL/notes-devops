# Notes DevOps

A simple Flask web application for managing personal notes, built to demonstrate
a complete educational DevOps pipeline for the course
«Современные проблемы программной инженерии» (Modern Problems of Software
Engineering), Peter the Great St. Petersburg Polytechnic University.

## Features

- Add, list and delete notes through a web interface
- Health check endpoint `GET /health`
- Prometheus metrics endpoint `GET /metrics` with custom business metrics:
  `notes_created_total`, `notes_deleted_total`, `notes_current`

## Tech stack

| Area | Tools |
|---|---|
| Application | Python 3.12, Flask, HTML/CSS |
| Testing | pytest |
| Version control | Git, GitHub, Git Flow (main / develop, tag v1.0) |
| Containerization | Docker, Docker Compose |
| CI | GitHub Actions (tests + Docker image build) |
| Orchestration | Kubernetes via Minikube (Deployment + NodePort Service) |
| Monitoring | Prometheus, Grafana |
| Configuration management | Ansible (Linux server scenario) |

## Project structure

```
notes-devops/
├── app.py                  # Flask application
├── requirements.txt        # Python dependencies
├── pytest.ini              # pytest configuration
├── Dockerfile              # application image
├── docker-compose.yml      # web + prometheus + grafana stack
├── .dockerignore
├── .github/workflows/ci.yml
├── templates/index.html    # UI template
├── static/style.css        # styles
├── tests/test_app.py       # automated tests
├── k8s/                    # Kubernetes manifests
├── prometheus/prometheus.yml
└── ansible/                # inventory + playbook
```

## Quick start

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py
# open http://127.0.0.1:5000
```

## Tests

```powershell
pytest
```

## CI

The GitHub Actions workflow `.github/workflows/ci.yml` runs on every push and
pull request to `main` and `develop`: installs dependencies, runs pytest and
builds the Docker image.
