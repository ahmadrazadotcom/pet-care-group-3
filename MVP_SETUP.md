# Pet Care Information System

ICT305 Software Development Project 2 – Group 3

This is the first working-code draft for the Sprint 1 MVP. Pet owners can use the website to keep their pet details, care records and appointments in one place. It uses Flask, SQLite, HTML, CSS and Bootstrap.

## What is included

| Story | Feature | Points |
|---|---|---:|
| US-01 | Create an account | 3 |
| US-02 | Sign in and sign out | 3 |
| US-03 | Add and view pets | 3 |
| US-04 | Edit pet details | 2 |
| US-05 | Add a care record | 5 |
| US-07 | Add a clinic appointment | 3 |
| US-09 | Show upcoming and overdue reminders | 5 |

The seven stories total 24 points. This is the planned scope, not a claim that the team completed or accepted all 24 points during the sprint. Editing or deleting care records and changing or cancelling appointments are planned for Sprint 2. No medical advice, payments, clinic portal or email/SMS reminders are included.

## Run on your computer

Install Python 3.12 or later. Open a terminal in this folder. On Windows, run:

```powershell
py -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe app.py
```

On macOS or Linux, run:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python app.py
```

Open http://127.0.0.1:5000 in a browser. Create a new account. The database is created automatically in the `instance` folder. Use made-up data only.

## Run tests

On Windows:

```powershell
.venv\Scripts\python.exe -m playwright install chromium
.venv\Scripts\python.exe -m pytest -v --cov=core --cov=app --cov-report=term-missing
```

On macOS or Linux:

```bash
.venv/bin/python -m playwright install chromium
.venv/bin/python -m pytest -v --cov=core --cov=app --cov-report=term-missing
```

The GitHub Actions workflow runs these tests on pushes and pull requests. A green result is only evidence once the workflow has actually run. If the repository already has a CI workflow, keep it until you confirm the new one works.

## Staging setup

Use a shared Python hosting environment with HTTPS and a persistent SQLite database. Install `requirements.txt`, use the start command `gunicorn --workers 1 --bind 0.0.0.0:$PORT app:app` (adapt the port to your host), and set these environment variables in the host's settings:

- `SECRET_KEY`: a long random secret, shared across restarts. Generate it locally with `python -c "import secrets; print(secrets.token_hex(32))"`. Never commit the value.
- `COOKIE_SECURE`: `1` when using HTTPS.
- `DATABASE_PATH`: a file path on a persistent writable volume, such as `/data/petcare.sqlite3` if the host mounts `/data`.

If the host has no persistent disk, data may be lost when the app restarts. Do not use real client information or personal pet records in the staging app. This is a teaching MVP, not a production service. The shared deployment has not been created or checked yet.

## Files

- `app.py`: web routes, sign-in checks and forms.
- `core.py`: database, passwords, input checks and reminder rules.
- `templates/`: HTML pages.
- `static/`: website styling.
- `tests/`: core, web integration and browser tests.
- `.github/workflows/pet-care-ci.yml`: automatic tests.

## AI use

ChatGPT helped prepare this initial code, tests and setup guide. Both students must review the files, run the tests and explain the parts they use. Record actual reviews and changes in the assessment's AI-use statement. Do not claim that unverified work has passed.
