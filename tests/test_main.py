import asyncio
import unittest.mock as mock

import asynctest
import pytest

from app import main
from tests import data
from tests import utils


@mock.patch("requests.post")
def test_authenticate_current_session_returns_ok(mock_requests):
    import requests

    term = {"code": "201904", "description": "Fall 2019 Quarter"}
    unique_session_id = "abcdef1234567890"
    cookies = {"JSESSIONID": "CF6813D3F9BFD1ABEEEF47E2FB094926"}
    response = requests.Response()
    response.status_code = 200
    mock_requests.return_value = response

    res = main.authenticate_current_session(term, unique_session_id, cookies)

    assert res.ok is True


@mock.patch("requests.post")
def test_authenticate_current_session_returns_not_ok_if_response_fails(mock_requests):
    import requests

    term = {"code": "201904", "description": "Fall 2019 Quarter"}
    unique_session_id = "abcdef1234567890"
    cookies = {"JSESSIONID": "CF6813D3F9BFD1ABEEEF47E2FB094926"}
    response = requests.Response()
    response.status_code = 400
    mock_requests.return_value = response

    res = main.authenticate_current_session(term, unique_session_id, cookies)

    assert res.ok is False


@mock.patch("requests.get")
def test_get_schedule_json_returns_ok_when_good_response(mock_requests):
    import json
    import requests

    subject = {"code": "CS", "description": "Computer Science"}
    term = {"code": "201904", "description": "Fall 2019 Quarter"}
    unique_session_id = "abcdef1234567890"
    cookies = {"JSESSIONID": "CF6813D3F9BFD1ABEEEF47E2FB094926"}
    response = requests.Response()
    response._content = bytearray(json.dumps(data.example_schedule), "utf-8")
    response.status_code = 200
    mock_requests.return_value = response

    schedule_json = main.get_schedule_json(subject, term, unique_session_id, cookies)

    assert schedule_json == data.example_schedule


@mock.patch("requests.get")
def test_get_schedule_json_returns_not_ok_when_bad_response(mock_requests):
    import requests

    subject = {"code": "CS", "description": "Computer Science"}
    term = {"code": "201904", "description": "Fall 2019 Quarter"}
    unique_session_id = "abcdef1234567890"
    cookies = {"JSESSIONID": "CF6813D3F9BFD1ABEEEF47E2FB094926"}
    response = requests.Response()
    response.status_code = 400
    mock_requests.return_value = response

    schedule_json = main.get_schedule_json(subject, term, unique_session_id, cookies)

    assert schedule_json is None


@mock.patch("requests.get")
def test_get_subjects_returns_json_response_when_response_ok(mock_requests):
    import json
    import requests

    cookies = {"cookie": "jar"}
    unique_session_id = "abcdef1234567890"
    term_date = "201904"
    subjects_response = [{"code": "ACTG", "description": "Accounting"}]
    response = requests.Response()
    response._content = bytearray(json.dumps(subjects_response), "utf-8")
    response.status_code = 200
    mock_requests.return_value = response

    subjects = main.get_subjects(cookies, unique_session_id, term_date)

    assert subjects == subjects_response


@mock.patch("requests.get")
def test_get_subjects_returns_none_when_response_ok(mock_requests):
    import json
    import requests

    cookies = {"cookie": "jar"}
    unique_session_id = "abcdef1234567890"
    term_date = "201904"
    subjects_response = [{"code": "ACTG", "description": "Accounting"}]
    response = requests.Response()
    response._content = bytearray(json.dumps(subjects_response), "utf-8")
    response.status_code = 400
    mock_requests.return_value = response

    subjects = main.get_subjects(cookies, unique_session_id, term_date)

    assert subjects is None


@pytest.mark.asyncio
@asynctest.patch("app.main.authenticate_current_session")
@asynctest.patch("app.main.get_schedule_json")
@asynctest.patch("app.pyppeteer.get_unique_session_id")
async def test_get_subjects_json_returns_data(
    mock_get_unique_session_id, mock_get_schedule_json, mock_authenticate
):
    subjects = [
        {"code": "ACTG", "description": "Accounting"},
        {"code": "ACTG", "description": "Accounting"},
    ]
    term = {"code": "201904", "description": "Fall 2019 Quarter"}
    cookies = {"cookie": "jar"}
    unique_session_id = "abcdef1234567890"
    mock_get_unique_session_id = asynctest.CoroutineMock()
    mock_get_unique_session_id = utils.set_async_result(
        mock_get_unique_session_id, unique_session_id
    )
    mock_get_schedule_json.return_value = {"data": "foo"}

    subjects_json = await main.get_subjects_json(subjects, term, cookies, None)

    assert "foo" in subjects_json
    assert len(subjects_json) == 2


@pytest.mark.asyncio
@asynctest.patch("app.main.authenticate_current_session")
@asynctest.patch("app.main.get_schedule_json")
@asynctest.patch("app.pyppeteer.get_unique_session_id")
async def test_get_subjects_json_returns_none_when_no_data(
    mock_get_unique_session_id, mock_get_schedule_json, mock_authenticate
):
    subjects = [
        {"code": "ACTG", "description": "Accounting"},
        {"code": "ACTG", "description": "Accounting"},
    ]
    term = {"code": "201904", "description": "Fall 2019 Quarter"}
    cookies = {"cookie": "jar"}
    unique_session_id = "abcdef1234567890"
    mock_get_unique_session_id = asynctest.CoroutineMock()
    mock_get_unique_session_id = utils.set_async_result(
        mock_get_unique_session_id, unique_session_id
    )
    mock_get_schedule_json.return_value = {}

    subjects_json = await main.get_subjects_json(subjects, term, cookies, None)

    assert subjects_json == []


@mock.patch("requests.get")
def test_get_terms_returns_json_response_when_response_ok(mock_requests):
    import json
    import requests

    cookies = {"cookie": "jar"}
    unique_session_id = "abcdef1234567890"
    terms_response = [{"code": "201904", "description": "Fall 2019 Quarter"}]
    response = requests.Response()
    response._content = bytearray(json.dumps(terms_response), "utf-8")
    response.status_code = 200
    mock_requests.return_value = response

    terms = main.get_terms(cookies, unique_session_id)

    assert terms == terms_response


@mock.patch("requests.get")
def test_get_terms_returns_none_when_response_not_ok(mock_requests):
    import json
    import requests

    cookies = {"cookie": "jar"}
    unique_session_id = "abcdef1234567890"
    terms_response = [{"code": "201904", "description": "Fall 2019 Quarter"}]
    response = requests.Response()
    response._content = bytearray(json.dumps(terms_response), "utf-8")

    response.status_code = 400
    mock_requests.return_value = response

    terms = main.get_terms(cookies, unique_session_id)

    assert terms is None


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
