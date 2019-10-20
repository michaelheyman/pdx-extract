from app import pyppeteer
from app import storage
from app.logger import logger


async def run():
    browser = await pyppeteer.initialize()
    page = await pyppeteer.get_page(browser)

    timestamp = await page.evaluate("new Date().toISOString()")
    payload = {"timestamp": timestamp}
    logger.debug(timestamp)
    logger.debug("Finished")
    storage.upload_to_bucket(payload)
    return payload
