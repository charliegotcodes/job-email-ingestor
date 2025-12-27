# Job Email Ingestor

A Python tool that connects to Gmail and ingests job-related emails into a structured format.

This project is part of a larger job-tracking system and is designed to:
- Read recent emails from Gmail
- Normalize key fields (sender, subject, date, snippet)
- Serve as a foundation for job application tracking automation

---

## Current Features

- Gmail OAuth authentication
- Fetches recent emails using the Gmail API
- Parses and normalizes email metadata:
  - Sender
  - Subject
  - Date
  - Snippet preview
- Clean, modular architecture (client / reader separation)

---
TBC