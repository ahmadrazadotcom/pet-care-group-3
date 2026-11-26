# Pet Care Information System – Group 3

ICT305 Software Development Project 2 – Assessment 2

The Pet Care Information System helps pet owners keep their pet details, care records and clinic appointments in one place. The website uses Python Flask, SQLite, HTML, CSS and Bootstrap.

## Sprint 1 Features

| Story ID | Feature | Story Points |
|---|---|---:|
| US-01 | Create an account | 3 |
| US-02 | Sign in and sign out | 3 |
| US-03 | Add and view pets | 3 |
| US-04 | Edit pet details | 2 |
| US-05 | Add care records | 5 |
| US-07 | Add clinic appointments | 3 |
| US-09 | View upcoming and overdue reminders | 5 |
| | Total planned points | 24 |

The first version includes the seven planned MVP features. Automated tests have passed. Team review and final acceptance are still required.

Editing care records and changing or cancelling appointments are planned for Sprint 2.

## Technologies Used

- Python Flask
- SQLite
- HTML and CSS
- Bootstrap
- Pytest
- Playwright
- GitHub Actions

## Run the Website

Install Python 3.12 or later. Open a terminal in the project folder.

### Windows

```
py -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe app.py
```

### macOS or Linux

```
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python app.py
```

Open http://127.0.0.1:5000 in a web browser.

Create an account to start using the website. The database is created automatically in the instance folder. Use sample data for testing.

## Automated Testing

The project uses Pytest and Playwright to test the website. GitHub Actions runs the tests when changes are pushed or a pull request is created.

### Test Results

Results from 26 November 2026:

| Test Result | Value |
|---|---:|
| Total tests | 28 |
| Passed | 28 |
| Failed | 0 |
| app.py coverage | 97% |
| core.py coverage | 100% |
| Combined coverage | 98% |

### Run Tests on Windows

```
.venv\Scripts\python.exe -m playwright install chromium
.venv\Scripts\python.exe -m pytest -v --cov=core --cov=app --cov-report=term-missing
```

### Run Tests on macOS or Linux

```
.venv/bin/python -m playwright install chromium
.venv/bin/python -m pytest -v --cov=core --cov=app --cov-report=term-missing
```

## Deployment

The website is planned for deployment in a shared hosting environment.

Start command:

```
gunicorn --workers 1 --bind 0.0.0.0:$PORT app:app
```

Environment variables:

- SECRET_KEY – a secure random key.
- COOKIE_SECURE – set to 1 when using HTTPS.
- DATABASE_PATH – a writable database file path on persistent storage.

Secret keys must not be added to GitHub. The staging website should only use sample data. A persistent disk is needed to keep records after the website restarts.

Deployment status: Pending.

## Project Files

- app.py – website functions and forms.
- core.py – database and application logic.
- templates/ – website pages.
- static/ – website styling.
- tests/ – automated tests.
- .github/workflows/ – GitHub Actions workflows.

## Project Documents

- WORKING_AGREEMENT.md
- DEFINITION_OF_DONE.md
- backlog.csv
- SETUP_GUIDE.md
- MVP_SETUP.md

## AI Use

ChatGPT was used to help prepare the initial code, tests and documentation. Automated tests were run through GitHub Actions. Team members must review and understand the code before final submission. AI use will be recorded in the assessment report.
