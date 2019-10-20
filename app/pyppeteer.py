import pyppeteer

INIT_URL = "https://www.google.com"


async def initialize():
    """Initializes pyppeteer browser with options.

    Doesn't open or close browser, that responsibility is left to the caller.

    Returns:
        Browser: A Pyppeteer browser.
    """
    args = ["--no-sandbox", "--disable-setuid-sandbox", "--ignore-certificate-errors"]
    browser = await pyppeteer.launch(args=args, headless=True)

    return browser


async def get_page(browser):
    """ Accesses a page via the Pyppeteer browser.

    Parameters:
        Browser: A Pyppeteer browser.
    """
    page = await browser.newPage()
    await page.goto(INIT_URL)
    return page
