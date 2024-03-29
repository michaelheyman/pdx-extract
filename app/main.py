import time

import requests

from app import config
from app import pyppeteer
from app import sanitize
from app import storage
from app import urls
from app.logger import logger


def authenticate_current_session(term, unique_session_id, cookies):
    """Make a POST request that will authenticate the user with this JSESSIONID
    and uniqueSessionId and enable the sched_page GET request to return JSON

    :param term:              Term dictionary with code and description keys.
    :param unique_session_id: Unique session id generated by the page which
                              allows authentication.
    :param cookies:           Cookies of the previous requests.
    """
    payload = {
        "dataType": "json",
        "endDatepicker": "",
        "startDatepicker": "",
        "studyPath": "",
        "studyPathText": "",
        "term": term["code"],
        "uniqueSessionId": unique_session_id,
    }
    return requests.post(
        urls.SEARCH_URL,
        headers={"Referer": urls.INIT_URL},
        cookies=cookies,
        params=payload,
    )


def get_schedule_json(subject, term, unique_session_id, cookies):
    """Gets JSON representation of the subject for the specified term.

    :param subject:           The subject in question.
    :param term:              The term in question.
    :param unique_session_id: Unique session id generated by the page which
                              allows authentication.
    :param cookies:           Cookies of the previous requests.
    """
    payload = {
        "txt_subject": subject["code"],
        "txt_term": term["code"],
        "startDatepicker": "",
        "endDatepicker": "",
        "uniqueSessionId": unique_session_id,
        "pageOffset": "0",
        "pageMaxSize": "100",
        "sortColumn": "subjectDescription",
        "sortDirection": "asc",
    }
    res = requests.get(
        urls.SCHEDULE_URL,
        headers={"Referer": urls.CLASS_URL},
        cookies=cookies,
        params=payload,
    )

    if res.ok:
        return res.json()

    return None


def get_subjects(cookies, unique_session_id, term_date):
    """Gets the subjects that are available for a particular term.

    :param cookies:           Cookies needed to authenticate the request.
    :param unique_session_id: Parameter needed to authenticate the request.
    :param term_date:         Term where the subjects will be searched for.
    :returns:                 JSON with list of subjects
    """
    payload = {
        "uniqueSessionId": unique_session_id,
        "dataType": "json",
        "searchTerm": "",
        "term": term_date,
        "offset": "1",
        "max": config.MAX_SUBJECTS,
        # Query string params expect a timestamp with extra 3 digits
        "_:": str(int(time.time() * 1000)),
    }
    res = requests.get(urls.SUBJECTS_URL, cookies=cookies, params=payload)

    if not res.ok:
        return None

    return res.json()


def get_terms(cookies, unique_session_id):
    """Gets JSON with list of terms in the form {code : description}

    :param cookies:           Cookies needed to authenticate the request
    :param unique_session_id: Parameter needed to authenticate the request
    :returns:                 JSON with list of the terms
    """
    payload = {
        "uniqueSessionId": unique_session_id,
        "dataType": "json",
        "searchTerm": "",
        "offset": "1",
        "max": config.MAX_TERMS,
    }
    res = requests.get(urls.TERMS_URL, cookies=cookies, params=payload)

    if res.ok:
        return res.json()

    logger.info("No terms were found.")
    return None


async def run():
    browser = await pyppeteer.initialize()
    page = await pyppeteer.get_page(browser)
    session_id, unique_session_id = await pyppeteer.get_tokens(browser)

    if None in (session_id, unique_session_id):
        browser.close()
        logger.error("Failed to get tokens from session.")
        return

    cookies = dict(JSESSIONID=session_id)
    terms = get_terms(cookies, unique_session_id)

    payload = {}
    for term in terms:
        subjects = get_subjects(cookies, unique_session_id, term["code"])
        subjects_json = await get_subjects_json(subjects, term, cookies, page)
        courses = sanitize.get_courses(subjects_json)
        payload[term["code"]] = courses

    [storage.upload_to_bucket({key: value}) for key, value in payload.items()]

    await browser.close()
    return payload


async def get_subjects_json(subjects, term, cookies, page):
    """Gets the JSON representation from each subject that is crawled.

    :param subjects: List of subjects
    :param term:     Term dictionary containing code and description
    :param cookies:  Page cookies
    :param page:     Pyppeteer page
    :return:         JSON list of the subjects crawled
    """
    subjects_json = []
    for idx, subject in enumerate(subjects):
        logger.debug(
            "Crawling subject",
            extra={
                "subject": subject["description"],
                "subjectIndex": idx + 1,
                "totalSubjects": len(subjects),
                "term": term["description"],
            },
        )

        unique_session_id = await pyppeteer.get_unique_session_id(page)
        authenticate_current_session(term, unique_session_id, cookies)
        sched_json = get_schedule_json(subject, term, unique_session_id, cookies)

        if "data" in sched_json.keys():
            subjects_json.append(sched_json["data"])
        else:
            logger.warning(
                "No course data found.", extra={"subject": subject["description"]}
            )

    return subjects_json
