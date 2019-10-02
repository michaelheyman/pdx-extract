# POC Google Function

POC to show Cloud Functions depositing JSON in Cloud Storage.

## Deploying

```bash
gcloud functions deploy run --memory=1024MB --runtime python37 --trigger-http --region us-central1
```
