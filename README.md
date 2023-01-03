# A python script that scrapes student's public data of BUBT

## Install the requirements
`pip install -r requirements.txt`

## Configuration
Create `config.toml` file by copying `config_sample.toml`. The config has 2 keys.
- `semesters` - (Array) of semesters that should be searched (Only required for `students.py`)
- `sqlite_path` - (String) that contains the path for sqlite database. This file will automatically be created if doesn't exist

## Run the script
`students.py` works for older semester untill "Spring 2019"
`students_v2.py` works for currently running semesters. No specification for semesters is required.


The script will ignore entries if it alraedy exist so there will be no duplicate entries.

## How it works
- Step 1 - The script crawls through BUBT's website which contains the results for each semester
- Step 2 - Download the pdf result sheet for a section
- Step 3 - Parse the first id from the result sheet
- Step 4 - Make API request to fetch student's data using the id
- Step 5 - Insert the data into sqlite database if it's unique
- Step 6 - Increase the integer value of id by 1. To target the next student
- Step 7 - Go to step 4
- Step 8 - If 5 consecutive id receives not found response than move to the next result sheet and go to step 2
- Step 9 - Exit when all the results sheets are scanned



> :warning: **The script was written for educational purpose only.**: It only fetches the data that are publicly made available by BUBT. The autohor of this repository will not be responsible for any harmful use of this script!