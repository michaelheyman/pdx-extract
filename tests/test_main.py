import asyncio

import asynctest
import pytest

from app import main


def set_async_result(mock, result):
    mock.return_value = asyncio.Future()
    mock.return_value.set_result(result)
    return mock


@pytest.mark.asyncio
@asynctest.patch("pyppeteer.launch")
async def test_initialize_browser_returns_browser(mock_launch):
    mock_launch = set_async_result(mock_launch, "mock-browser")

    browser = await main.initialize_browser()

    mock_launch.assert_called
    assert browser == "mock-browser"


@pytest.mark.asyncio
@asynctest.patch("app.storage.upload_to_bucket")
@asynctest.patch("app.main.get_page")
@asynctest.patch("app.main.initialize_browser")
async def test_run_returns_payload(
    mock_initialize, mock_get_page, mock_upload_to_bucket
):
    mock_initialize = set_async_result(mock_initialize, [])
    get_page = asynctest.CoroutineMock()
    get_page.evaluate.return_value = asyncio.Future()
    get_page.evaluate.return_value.set_result("foo")
    mock_get_page = set_async_result(mock_get_page, get_page)
    mock_upload_to_bucket().return_value = None

    result = await main.run()

    mock_initialize.assert_called
    mock_get_page.assert_called
    get_page.assert_called
    mock_upload_to_bucket.assert_called
    assert result == {"timestamp": "foo"}
