import json
from datetime import datetime
from google.cloud import storage
from google.cloud import exceptions

storage_client = storage.Client()


def upload_to_bucket(contents):
    assert isinstance(contents, dict)
    bucket_name = "my-different-bucket"
    bucket = storage_client.lookup_bucket(bucket_name)

    if bucket is None:
        bucket = storage_client.create_bucket(bucket_name)
        print("Bucket {} created.".format(bucket.name))
    else:
        print("Bucket {} already exists.".format(bucket.name))

    timestamp = int(datetime.now().timestamp())
    filename = f"{timestamp}.json"
    lambda_filename = f"/tmp/{filename}"

    with open(lambda_filename, "w") as outfile:
        json.dump(contents, outfile)

    print(f"file: {outfile}")
    blob = bucket.blob(filename)
    blob.upload_from_filename(lambda_filename)

    print("File {} uploaded to {}.".format(filename, bucket_name))


def write_to_file(filename):
    with open(filename, "w") as outfile:
        json.dump(
            {
                "timestamp": timestamp,
                "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            },
            outfile,
        )
    print(f"file: {outfile}")


if __name__ == "__main__":
    bucket_name = "my-different-bucket"
    bucket = storage_client.lookup_bucket(bucket_name)

    if bucket is None:
        bucket = storage_client.create_bucket(bucket_name)
        print("Bucket {} created.".format(bucket.name))
    else:
        print("Bucket {} already exists.".format(bucket.name))

    timestamp = int(datetime.now().timestamp())
    filename = f"{timestamp}.json"
    file_contents = json.dumps({"timestamp": timestamp})

    write_to_file(filename)

    blob = bucket.blob(filename)
    blob.upload_from_filename(filename)
    blob.upload_from_string(json.dumps(file_contents), content_type="application/json")

    print("File {} uploaded to {}.".format(filename, bucket_name))
