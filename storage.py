import config
import json
from datetime import datetime
from google.cloud import storage
from google.cloud import exceptions

storage_client = storage.Client()


def upload_to_bucket(contents):
    """
    Uploads contents to Cloud Storage bucket.

    Parameters:
        contents (Object): The contents to put in the bucket
    """
    assert isinstance(contents, dict)
    bucket_name = config.BUCKET_NAME
    bucket = storage_client.lookup_bucket(bucket_name)

    if bucket is None:
        bucket = storage_client.create_bucket(bucket_name)
        print("Bucket {} created.".format(bucket.name))
    else:
        print("Bucket {} already exists.".format(bucket.name))

    filename = generate_filename()

    lambda_filename = write_lambda_file(filename, contents)

    blob = bucket.blob(filename)
    # uploads the file in the cloud function to cloud storage
    blob.upload_from_filename(lambda_filename)

    print("File {} uploaded to {}.".format(filename, bucket_name))


def write_lambda_file(filename, contents):
    """ Saves content to lambda filename.

    Saves contents to a filename and writes them to a /tmp/ directory in the Cloud Function.
    Cloud Functions only have write access to their /tmp/ directory.

    Parameters:
        filename (String): The filename to write the data to.
        contents (Object): The contents to put in the bucket.
    """
    lambda_filename = f"/tmp/{filename}"

    with open(lambda_filename, "w") as outfile:
        json.dump(contents, outfile)

    print(f"file: {outfile}")

    return lambda_filename


def generate_filename():
    """ Generates a filename to be put into a Storage bucket.

    Returns:
        String: A filename in the format epoc.json
        Example:
            137281912.json
    """
    date_format = "%Y%m%d%H%M%S"
    timestamp = datetime.now().timestamp()
    date = datetime.fromtimestamp(timestamp).strftime(date_format)

    return f"{date}.json"


def write_to_file(filename, timestamp):
    """ Writes a timestamp and current date to a file.

    Only used when testing storage.py

    Parameters:
        filename (String): The filename to write the data to.
        timestamp (Int):   The epoch timestamp.
    """
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
    bucket_name = config.BUCKET_NAME
    bucket = storage_client.lookup_bucket(bucket_name)

    if bucket is None:
        bucket = storage_client.create_bucket(bucket_name)
        print("Bucket {} created.".format(bucket.name))
    else:
        print("Bucket {} already exists.".format(bucket.name))

    timestamp = int(datetime.now().timestamp())
    filename = f"{timestamp}.json"
    file_contents = json.dumps({"timestamp": timestamp})

    write_to_file(filename, timestamp)

    blob = bucket.blob(filename)
    blob.upload_from_filename(filename)
    blob.upload_from_string(json.dumps(file_contents), content_type="application/json")

    print("File {} uploaded to {}.".format(filename, bucket_name))
