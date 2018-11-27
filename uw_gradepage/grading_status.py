
"""
This is the interface for interacting with the GradePage Web Service.
"""

from dateutil.parser import parse
from logging import getLogger
from uw_gradepage.models import GradingStatus
from uw_gradepage import get_resource
from urllib.parse import quote

GRADING_STATUS_URL = "/api/v1/grading_status/{section_id}"
logger = getLogger(__name__)


def get_grading_status(section_id, act_as=None):
    """
    Return a restclients.models.gradepage.GradePageStatus object
    on the given course
    """
    url = GRADING_STATUS_URL.format(section_id=quote(section_id))
    headers = {}

    if act_as is not None:
        headers["X-UW-Act-as"] = act_as

    return _object_from_json(url, get_resource(url, headers))

def _object_from_json(url, json_data):
    return_obj = GradingStatus()

    gs_data = json_data.get('grading_status')
    return_obj.section_id = gs_data['section_id']
    return_obj.grading_period_open = gs_data['grading_period_open']
    return_obj.display_name = gs_data['display_name']
    return_obj.section_url = gs_data['section_url']
    return_obj.status_url = gs_data['status_url']
    return_obj.grading_status = gs_data['grading_status']

    try:
        return_obj.submitted_count = gs_data['submitted_count']
        return_obj.unsubmitted_count = gs_data['unsubmitted_count']
        return_obj.submitted_by = gs_data['submitted_by']
        return_obj.submitted_date = parse(gs_data["submitted_date"])
        return_obj.accepted_date = parse(gs_data["accepted_date"])
        return_obj.no_grades_submitted = False
    except KeyError:
        return_obj.no_grades_submitted = True

    return return_obj