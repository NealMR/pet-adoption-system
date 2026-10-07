# Pet Adoption & Management System — DevOps Mini Project

## Purpose
The goal of this project is to build a robust Pet Adoption REST API that allows users to register pets for adoption, submit adoption requests, and manage adoption approvals, all while utilizing a complete DevOps pipeline for CI/CD and deployment.

## Team Members

| Role ID | Name | Role | Responsibility | Technologies |
|---------|------|------|----------------|--------------|
| S1 | Neal | Product Owner / Team Lead | Project Documentation | Markdown, Mermaid |
| S2 | Sagar | Developer 1 | Pet Registration Module | Python, FastAPI, Pydantic |
| S3 | Yash | Developer 2 | Adoption Request Module | Python, FastAPI, Pydantic |
| S4 | Harshwardhan | Developer 3 | Admin Management + App Entry Point | Python, FastAPI |
| S5 | Jyotiraditya | QA Engineer | Test Suite & Requirements | Pytest, Python |
| S6 | Atharv | Git Engineer | Version Control Setup | Git, GitHub |
| S7 | Omkar | Jenkins Engineer | CI/CD Pipeline | Jenkins, Groovy |
| S8 | Tanishq | Docker Engineer | Containerization | Docker |
| S9 | Siddhik | Kubernetes Engineer | Orchestration Manifests | Kubernetes, YAML |
| S10 | Rushikesh | DevOps/SRE Engineer | Final Documentation | Markdown, Git |

## GitFlow Strategy

Our team follows a structured GitFlow strategy to ensure code quality and seamless collaboration:

- **main branch:** This is the production-ready branch. Code here is always stable and deployable.
- **develop branch:** This serves as the integration branch for all features. It reflects the latest delivered development changes for the next release.
- **feature branches:** Developers create individual feature branches (e.g., `feature/S1`, `feature/S2`) off the `main` or `develop` branch to work on their specific tasks. Once the task is complete, a Pull Request is opened to merge the changes into `develop` or `main`. Code reviews and CI pipeline checks must pass before merging.
