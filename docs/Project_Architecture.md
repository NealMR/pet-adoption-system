# Project Architecture

## High-Level API Architecture

```mermaid
flowchart LR
    A[Client] -->|HTTP Requests| B[Kubernetes Service]
    B --> C[FastAPI Pod 1]
    B --> D[FastAPI Pod 2]
    C --> E[(In-Memory DB)]
    D --> E[(In-Memory DB)]
```

## CI/CD Pipeline Diagram

```mermaid
flowchart TD
    A[Developer Push] --> B[GitHub Repository]
    B -->|Webhook Trigger| C[Jenkins Pipeline]
    C --> D[Pytest Tests]
    D -->|If Tests Pass| E[Docker Build]
    E --> F[Push to Registry]
    F --> G[K8s Deploy]
```

## Tech Stack

| Layer | Technology | Purpose |
|-------|------------|---------|
| Backend | Python 3.9+ | Core programming language |
| API Framework | FastAPI & Pydantic | Building the REST API and data validation |
| Testing | Pytest | Automated testing for API endpoints |
| Version Control | Git & GitHub | Source code management and collaboration |
| CI/CD | Jenkins | Continuous Integration and Deployment pipeline |
| Containerization | Docker | Packaging the application into portable containers |
| Orchestration | Kubernetes | Deploying, scaling, and managing the containers |
