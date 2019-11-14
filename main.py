import asyncio

from app import main


def extract(event, context):
    """Background Cloud Function to be triggered by Pub/Sub.

    Docstrings take from: https://cloud.google.com/functions/docs/calling/pubsub

    :param event: The dictionary with data specific to this type of event.
                  The `data` field contains the PubsubMessage message. The
                  `attributes` field will contain custom attributes if there
                  are any.
    :param context: The Cloud Functions event metadata. The `event_id` field
                    contains the Pub/Sub message ID. The `timestamp` field
                    contains the publish time.
    :return: None
    """
    asyncio.get_event_loop().run_until_complete(main.run())
