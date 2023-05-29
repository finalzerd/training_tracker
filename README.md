# FJ Training Tracker

This repo is used to  to track the progress of applicants' udemy and youtube courses on a google sheet and reset the courses as needed.

# Setup Instructions
```
git clone <repo-link>
cd training_tracker
python3 -m venv .venv
source venv/bin/activate # for linux
venv\Scripts\Activate.ps1 # for windows
pip install -r requirements.txt
```

# Runnable Scripts
Running with the --test flag will use the test config file instead of the default config file this is useful for testing the scripts without affecting the actual google sheet
```
python daily_tracker.py [-h] [--test TEST]
```
this is the main script that will be used to track the progress of the applicants. It will check the udemy and youtube courses and update the google sheet accordingly. It will also reset the courses if needed.

```
python offline_tracker.py [-h] [--test TEST]
```
TODO: fill in
```
python auto_reports.py [-h] [--test TEST]
```
TODO: fill in

