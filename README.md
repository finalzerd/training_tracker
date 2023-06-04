# FJ Training Tracker

This repo is used to periodically update the google sheets that track FJ trainees progress on udemy and youtube courses.

# Setup
```
git clone <repo-link>
cd training_tracker
git clone <fjutils-link>
python -m venv .venv
source .venv/bin/activate # for linux
.venv\Scripts\Activate.ps1 # for windows
pip install -r requirements.txt
```
Create a `.env` file following the same structure as `.env.example` and fill in the values.


# Execution
options:
  -h, --help            show this help message and exit
  --test, -t            to run with the test config in config/test_config.json
  --date DATE, -d DATE  to run with a specific date, must be in YYYY-MM-DD format
  --row ROW, -r ROW     run a specific row from the tracker sheet
## Daily Tracker
This script is used to track the progress of the applicants on online courses. Main functionality is to:
* Check the udemy and youtube courses and update the google sheet to reflect progress
* Reset the course on udemy if the applicant has completed the course
* Send a emails to applicants on course start, reminder, completion, and quiz

```
python src/daily_tracker.py [-h] [--test] [--date DATE] [--row ROW]
```
## Offline Tracker
TODO: fill in
```
python src/offline_tracker.py [-h] [--test] [--date DATE] [--row ROW]
```
## Auto Reports
This script is meant to be run weekly to generate the weekly course reports for the applicants. It will send a email with a dataframe in html to each applicant with the courses they are registered for on the google sheets.
```
python src/auto_reports.py [-h] [--test] [--date DATE] [--row ROW]
```

