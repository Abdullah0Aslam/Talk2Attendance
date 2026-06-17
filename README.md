# Talk2Attendance

> A friendly chatbot-powered attendance system for classrooms and teams.

## Why Talk2Attendance?

Talk2Attendance combines a conversational chatbot with a lightweight attendance backend so instructors and team leads can record and query attendance quickly—using natural language instead of forms.

## Features

- Chat-first attendance recording and queries
- Simple Python backend with pluggable storage (SQLite/Postgres)
- Clean schema and models for easy extension
- Ready for integration with messaging platforms or a web UI

## Tech Stack

- Python 3.9+
- Core modules: `chatbot.py`, `main.py`, `database.py`, `models.py`, `schemas.py`
- Requirements in `requirements.txt`

## Quickstart

1. Clone the repo:

```bash
git clone https://github.com/Abdullah0Aslam/Talk2Attendance.git
```

2. Create a Python virtual environment and install dependencies:

```bash
python -m venv .venv
.
# Windows PowerShell
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

3. Run the app (example):

```bash
python main.py
```

Tip: open `chatbot.py` and `prompt_templates.py` to see how the conversational prompts are structured.

## Usage

- Start the application and interact with the chatbot to record attendance (e.g., "Mark Alice present for Math, today").
- Ask natural-language queries such as "Who was absent yesterday?" or "Show attendance for class CS101 this month." 

## Configuration

- Database connection and other settings can be configured in `database.py` or via environment variables depending on your setup.
- To switch storage backends, update the connection logic in `database.py` and adjust `models.py` if necessary.

## Project Layout

- `main.py` — entry point
- `chatbot.py` — conversational interface and intent handling
- `database.py` — DB connection and persistence helpers
- `models.py` / `schemas.py` — data models and validation
- `prompt_templates.py` — chat prompts and templates
- `helpers.py` — utility helpers

## Contributing

Contributions welcome — please open issues or pull requests. Follow these steps:

1. Fork the repo
2. Create a feature branch (`git checkout -b feat/your-feature`)
3. Add tests and documentation
4. Open a PR describing your changes

