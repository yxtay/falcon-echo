import functools
import json
import traceback

import falcon

from src.utils.logger import logger
from src.utils.tracer import init_tracer, start_trace_span, trace_function


@trace_function
def get_falcon_resp(resp, data={}):
    body = {"status": falcon.HTTP_200}
    body.update(data)

    with start_trace_span("[logger.info]"):
        logger.info("response body", extra={"data": body})

    resp.body = json.dumps(body, default=str)
    resp.status = body["status"]
    return resp


@trace_function
def get_error_resp(resp, exception):
    with start_trace_span("[logger.exception]"):
        logger.exception(repr(exception), extra={"severity": "ERROR"})

    body = {
        "status": falcon.HTTP_500,
        "error": repr(exception),
        "traceback": traceback.format_exc().strip().split("\n"),
    }
    return get_falcon_resp(resp, body)


def add_trace_init(func):
    @functools.wraps(func)
    def wrapper(self, req, resp, *args, **kwargs):
        tracer = init_tracer()
        with tracer.span(req.uri):
            func(self, req, resp, *args, **kwargs)

        tracer.finish()

    return wrapper


def add_exception_handling(func):
    @functools.wraps(func)
    def wrapper(self, req, resp, *args, **kwargs):
        try:
            func(self, req, resp, *args, **kwargs)
        except Exception as e:
            get_error_resp(resp, e)

    return wrapper
