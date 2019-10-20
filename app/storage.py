import json
from datetime import datetime

from google.cloud import storage

from app import config
from app import utils


def upload_to_bucket(contents):
    """
    Uploads contents to Cloud Storage bucket.

    Parameters:
        contents (Object): The contents to put in the bucket
    """
    assert isinstance(
        contents, (dict, list)
    ), f"Expected dict/list but got {type(contents)}"
    storage_client = storage.Client()
    bucket_name = config.BUCKET_NAME
    bucket = storage_client.lookup_bucket(bucket_name)

    if bucket is None:
        bucket = storage_client.create_bucket(bucket_name)
        print("Bucket {} created.".format(bucket.name))
    else:
        print("Bucket {} already exists.".format(bucket.name))

    filename = utils.generate_filename()

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


if __name__ == "__main__":
    storage_client = storage.Client()
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

    blob = bucket.blob(filename)
    blob.upload_from_filename(filename)
    blob.upload_from_string(json.dumps(file_contents), content_type="application/json")

    print("File {} uploaded to {}.".format(filename, bucket_name))
