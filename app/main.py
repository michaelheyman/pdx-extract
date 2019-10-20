import asyncio
import json
from app import sanitize
import pprint
import requests
from app.logger import logger
from app.storage import upload_to_bucket
from pyppeteer import launch

INIT_URL = "https://www.google.com"


async def initialize_browser():
    """Initializes pyppeteer browser with options.
    
    Doesn't open or close browser, that responsibility is left to the caller.

    Returns:
        Browser: A Pyppeteer browser.
    """
    args = ["--no-sandbox", "--disable-setuid-sandbox", "--ignore-certificate-errors"]
    browser = await launch(args=args, headless=True)

    return browser


async def get_page(browser):
    """ Accesses a page via the Pyppeteer browser.

    Parameters:
        Browser: A Pyppeteer browser.
    """
    page = await browser.newPage()
    await page.goto(INIT_URL)
    return page


async def run(context):
    browser = await initialize_browser()
    page = await get_page(browser)

    timestamp = await page.evaluate("new Date().toISOString()")
    payload = {"timestamp": timestamp}
    logger.debug(timestamp)
    logger.debug("Finished")
    upload_to_bucket(payload)


async def mockRun(context):
    with open("response.json") as json_file:
        terms = json.loads(json_file.read())

    subjects = []
    for term in terms:
        for subject in term:
            pp = pprint.PrettyPrinter(indent=2)
            # pp.pprint(terms[0]["data"][0])
            sanitized_data = sanitize.get_course_data(terms[0]["data"][0])
            pp.pprint(sanitized_data)
            subjects.append(sanitized_data)

    upload_to_bucket(subjects)
