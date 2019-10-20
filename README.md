# poc-google-function

[poc-google-function](https://github.com/michaelheyman/poc-google-function/) is part of the
[pdx-schedule](https://github.com/michaelheyman/pdx-schedule/) project.

Runs a Cloud Function that scrapes the schedule information from Portland State.
It then stores the JSON representation of the schedule into a Cloud Storage bucket.

## Setup

### Create Virtual Environment

```bash
pyenv virtualenv 3.7.3 poc-google-function-3.7.3
pyenv activate poc-google-function-3.7.3
```

### Install Requirements

```bash
pip -r install requirements.txt
```

### Install Git Hooks

See [.pre-commit-config.yaml](.pre-commit-config.yaml) for information on which hooks are configured.

```bash
pre-commit install
```

```bash
pre-commit install -t pre-push
```

## Running

Run the application by executing

```bash
python -m app
```

## Deploying

```bash
gcloud functions deploy run --memory=1024MB --runtime python37 --trigger-http --region us-central1
```

## JSON Fields

The PSU API returns JSON payloads with the following format:

```json
{
    "data": [
        {
            "term": "201904",
            "termDesc": "Fall 2019 Quarter",
            "courseReferenceNumber": "10883",
            "courseNumber": "161",
            "subject": "CS",
            "subjectDescription": "Computer Science",
            "courseTitle": "INTRO PROGRAM &amp; PROB SOLVING",
            "creditHours": 4,
            "faculty": [
                {
                    "displayName": "Ely, David D"
                }
            ],
            "meetingsFaculty": [
                {
                    "meetingTime": {
                        "beginTime": "1000",
                        "endTime": "1150",
                        "monday": true,
                        "tuesday": false,
                        "wednesday": false,
                    },
                }
            ],
        }
    ],
}
```

The goal is to transform them into this:

```json
[
    {
        "number": "CS 161",
        "name": "INTRO PROGRAM &amp; PROB SOLVING",
        "crn": "10883",
        "discipline": "Computer Science",
        "days": "M",
        "credits": 4,
        "time": "10:00 - 11:50",
        "instructor": "David Ely",
        "term_description": "Fall 2019",
        "term_date": "201904",
    }
]
```
