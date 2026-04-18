# LOTR.api

A full-stack Lord of the Rings themed web application built with **FastAPI**, **Tortoise ORM**, **PostgreSQL**, and a **Vanilla JavaScript** frontend.

This project lets users browse LOTR characters through a custom UI with character cards, modal details, and a deployed frontend/backend architecture on Render.

## Live Demo

- Frontend: https://lotr-api-frontend.onrender.com
- API Docs: https://lotr-api-gs1y.onrender.com/docs
- GitHub Repository: https://github.com/pavlapintaric235/LOTR.api

---

## Overview

LOTR.api is a portfolio project designed to demonstrate full-stack web development skills using a Python API backend and a separately deployed frontend.

The project includes:

- A **FastAPI** backend exposing character endpoints
- A **PostgreSQL** database for persistent storage
- **Tortoise ORM** models and schemas
- A **Vanilla JS** frontend that fetches character data from the API
- A responsive UI with character cards and modal details
- CI setup with **GitHub Actions**, **pytest**, **flake8**, **black**, and **isort**
- Docker-based development and deployment workflow
- A seed script to populate the database through the API

---

## Features

- Browse LOTR characters from a live API
- View character details in a modal
- Responsive card-based UI
- Separate frontend and backend deployments on Render
- Database-backed API with async ORM
- Seed script for loading initial character data
- CI pipeline for linting, formatting, and tests

---

## Tech Stack

### Backend
- FastAPI
- Tortoise ORM
- PostgreSQL
- Aerich (migrations)
- Uvicorn
- Docker

### Frontend
- HTML
- CSS
- Vanilla JavaScript

### DevOps / Tooling
- GitHub Actions
- pytest
- pytest-cov
- flake8
- black
- isort
- Render

---

## Project Structure

```text
LOTR.api/
├── .github/
│   └── workflows/          # CI configuration
├── data/                   # Seed/input data
├── frontend/               # Static frontend files
│   ├── index.html
│   ├── style.css
│   ├── app.js
│   └── images/
├── project/                # Backend application code
│   ├── app/
│   │   ├── api/
│   │   ├── models/
│   │   ├── config/
│   │   └── ...
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── seed_characters.py
└── README.md
```

## Screenshots

### Home Page
<p align="center">
<img src="https://github.com/user-attachments/assets/cc891823-7d25-4645-a8b0-73b03e03b155">
 <p/>



### Character Modal
<img width="2360" height="1535" alt="IMG_2602" src="https://github.com/user-attachments/assets/4a8d6da5-e5ea-4060-97a9-7dad5bc3200d" />


### API Docs
<img width="2360" height="1519" alt="IMG_2603" src="https://github.com/user-attachments/assets/868b6832-a181-4a3a-b2ed-3e500e6682bb" />

