import asyncio

import asynctest
import pytest

from app import main
from tests import utils


@pytest.mark.asyncio
@asynctest.patch("app.storage.upload_to_bucket")
@asynctest.patch("app.pyppeteer.get_page")
@asynctest.patch("app.pyppeteer.initialize")
async def test_run_returns_payload(
    mock_initialize, mock_get_page, mock_upload_to_bucket
):
    mock_initialize = utils.set_async_result(mock_initialize, [])
    get_page = asynctest.CoroutineMock()
    get_page.evaluate.return_value = asyncio.Future()
    get_page.evaluate.return_value.set_result("foo")
    mock_get_page = utils.set_async_result(mock_get_page, get_page)
    mock_upload_to_bucket().return_value = None

    result = await main.run()

    mock_initialize.assert_called
    mock_get_page.assert_called
    get_page.assert_called
    mock_upload_to_bucket.assert_called
    assert result == {"timestamp": "foo"}
