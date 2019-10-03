import asyncio
from logger import logger
from pyppeteer import launch
from storage import upload_to_bucket

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
    logger.log_text(timestamp)
    logger.log_text("Finished")
    upload_to_bucket(payload)


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(run(None))
