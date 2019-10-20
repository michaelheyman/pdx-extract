import asynctest
import pytest

from app import pyppeteer
from tests import utils


@pytest.mark.asyncio
@asynctest.patch("pyppeteer.launch")
async def test_initialize_browser_returns_browser(mock_launch):
    mock_launch = utils.set_async_result(mock_launch, "mock-browser")

    browser = await pyppeteer.initialize()

    mock_launch.assert_called
    assert browser == "mock-browser"
