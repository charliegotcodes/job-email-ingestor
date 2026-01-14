# Job Email Ingestor

A backend service that ingests job-related emails, classifies them into lifecycle events, and forwards structured data to a downstream Job Tracker API for persistence and analysis.

This project focuses on reliability, data normalization, and maintainable API-driven design, rather than UI.

## Overview

The Job Email Ingestor monitors incoming emails (e.g. application confirmations, rejections, interview requests), extracts relevant metadata, classifies the email into a job lifecycle stage, and emits a normalized event to a Job Tracker API.

It is designed to be:

* Idempotent (safe to reprocess emails)
* Extensible (new categories and providers can be added)
* Fault-tolerant (graceful handling of malformed data or API failures)

### Architecture
Email Source (Gmail API)
        |
        v
Email Fetcher & Parser
        |
        v
Classification Layer
        |
        v
Normalized Job Event
        |
        v
Job Tracker API (FastAPI)
        |
        v
Relational Database (PostgreSQL / SQLite)


### Tech Stack

Language: Python

Framework: FastAPI

Email Integration: Gmail API

Data Modeling: SQLModel

Databases: PostgreSQL (prod), SQLite (local/dev)

HTTP Client: Requests

Logging: Python logging module

Config Management: Environment variables (python-dotenv)

### Key Features

* Email ingestion pipeline that fetches and parses structured and unstructured email content
* Lifecycle classification (e.g. Applied, Interview, Rejected, Offer)
* Idempotent event delivery using external IDs to prevent duplicate records
* Schema validation to ensure data integrity before persistence
* Centralized logging and error handling for observability
* Decoupled architecture separating ingestion from storage

### Project Structure

job-email-ingestor/
├── ingestor/
│   ├── main.py            # Entry point
│   ├── clients/           # External service clients (Gmail, Job Tracker API)
│   ├── parsers/           # Email parsing and normalization logic
│   ├── classifiers/       # Job lifecycle classification rules
│   └── config.py          # Environment and settings
├── .env.example
├── requirements.txt
└── README.md

### Setup & Installation

1. Clone the repository

git clone https://github.com/charliegotcodes/job-email-ingestor.git
cd job-email-ingestor

2. Create and activate a virtual environment
   
python -m venv venv
source venv/bin/activate

3.Install dependencies

pip install -r requirements.txt

4.Configure environment variables
Create a .env file based on .env.example:

GMAIL_CLIENT_ID=your_client_id
GMAIL_CLIENT_SECRET=your_client_secret
JOB_TRACKER_API_URL=http://localhost:8000/events

Running the Ingestor
python -m ingestor.main

The service will:
1. Fetch new emails
2. Parse and classify job-related messages
3. Send normalized lifecycle events to the Job Tracker API

#### Error Handling & Reliability

* Emails that fail parsing are logged and skipped without stopping the pipeline
* Duplicate emails are ignored via idempotent event keys
* Downstream API failures are logged with retry-safe behavior

### Future Improvements

* Rule-based → ML-assisted classification
* Support for additional email providers
* Retry queue for transient API failures
* Metrics and health-check endpoints
* Webhook-based ingestion instead of polling
