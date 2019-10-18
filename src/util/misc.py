import json
import traceback

import falcon
from opencensus.trace.execution_context import get_opencensus_tracer

from src.util.logger import logger
from src.util.tracer import get_frame_name, trace_function


@trace_function
def get_falcon_resp(resp, data={}):
    body = {
        "status": falcon.HTTP_200,
        "status_code": 200,
        "message": "ok",
    }
    body.update(data)

    with get_opencensus_tracer().span(get_frame_name() + "[logger.info]"):
        logger.info("response body", extra={"data": body})

    resp.body = json.dumps(body, default=str)
    resp.status = body["status"]
    return resp


@trace_function
def get_error_resp(resp, exception):
    with get_opencensus_tracer().span(get_frame_name() + "[logger.exception]"):
        logger.exception(exception, extra={"severity": "ERROR"})

    body = {
        "status": falcon.HTTP_500,
        "status_code": 500,
        "message": "internal server error",
        "error": repr(exception),
        "traceback": traceback.format_exc().strip().split("\n"),
    }
    return get_falcon_resp(resp, body)
