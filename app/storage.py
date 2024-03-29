import json

from google.cloud import storage

from app import config
from app import utils
from app.logger import logger


def upload_to_bucket(contents):
    """Uploads contents to Cloud Storage bucket.

    :param contents: The contents to put in the bucket
    :return:         None
    """
    assert isinstance(contents, dict), f"Expected dict but got {type(contents)}"
    storage_client = storage.Client()
    bucket_name = config.BUCKET_NAME
    bucket = storage_client.lookup_bucket(bucket_name)

    if bucket is None:
        bucket = storage_client.create_bucket(bucket_name)
        logger.debug("Bucket {} created.".format(bucket.name))
    else:
        logger.debug("Bucket {} already exists.".format(bucket.name))

    filename = utils.generate_filename()
    term_code = next(iter(contents))

    lambda_filename = write_lambda_file(filename, contents)

    blob = bucket.blob(filename)
    # uploads the file in the cloud function to cloud storage
    blob.upload_from_filename(lambda_filename)
    renamed_filename = f"{term_code}/{filename}"
    bucket.rename_blob(blob, renamed_filename)

    logger.debug("File {} uploaded to {}.".format(renamed_filename, bucket_name))


def write_lambda_file(filename, contents):
    """Saves content to lambda filename.

    Saves contents to a filename and writes them to a /tmp/ directory in the Cloud Function.
    Cloud Functions only have write access to their /tmp/ directory.

    :param filename: The filename to write the data to.
    :param contents: The contents to put in the bucket.
    :return:         The created lambda filename
    """
    lambda_filename = f"/tmp/{filename}"

    with open(lambda_filename, "w") as outfile:
        json.dump(contents, outfile)

    return lambda_filename
