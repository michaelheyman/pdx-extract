# POC Google Function

POC to show Cloud Functions depositing JSON in Cloud Storage.

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
