# TestMe app
QA Mania  
https://qamania.org/

## About
The main goal of this application - learn how to cover web apps with autotests.
It is designed to be cross platform and does not require many dependencies.  
_Application code is not optimal due to design restrictions but expected to be good enough for autotests_  

## Application Description
TestMe - simple test management system. It provides features to create, update, delete, run and view list of test cases.
Also it is possible to view list of all test runs and get stats of all test cases in the system.
Demo features designed additionally to give automation test engineers possibility to handle 
long waitings and multiple ajax requests

### Features
- Registration
- Login
- View Test Stats
- List test cases
- Create test case
- Update test case
- Delete test case
- Run test case (make it pass or fail)
- Download test cases to csv file
- Upload test cases as csv file  
- List test runs
- Open page after specific BE delay
- Open page and wait specific number of ajax requests handled
- Handle HTTP 500 errors


## Application has:  
- Web UI
- Mobile version of web UI
- coordinates in UI header for location tests   
- REST services
- SQLite DB to work with DB without installing 3rd party services
- Page with different input types to play with

## Preconditions
- Python 3.8+
- Install Django using `pip install -r requirements.txt`
- Free network port 8000

## How to run
1. Open CLI
2. Navigate to project folder
3. Execute command: `python manage.py runserver`  

Server will be started at http://127.0.0.1:8000  

## Default users
- alice
- bob
- charlie  

password: _Qamania123_


