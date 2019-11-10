import json

import falcon

from src.misc import multi_sleep
from src.request import Request
from src.util import falcon as falcon_util


class HealthResource(object):
    def on_get(self, req, resp):
        body = {"status": falcon.HTTP_200}
        resp.body = json.dumps(body)


class HelloResource(object):
    @falcon_util.add_trace_init
    def on_get(self, req, resp):
        falcon_util.get_falcon_resp(resp, {"message": "hello"})


class EchoResource(object):
    @falcon_util.add_trace_init
    @falcon_util.add_exception_handling
    def on_get(self, req, resp):
        request = Request.from_falcon_req(req)
        falcon_util.get_falcon_resp(resp, request.attributes)

    @falcon_util.add_trace_init
    @falcon_util.add_exception_handling
    def on_post(self, req, resp):
        request = Request.from_falcon_req(req)
        falcon_util.get_falcon_resp(resp, request.attributes)


class ParalleliseResource(object):
    @falcon_util.add_trace_init
    @falcon_util.add_exception_handling
    def on_get(self, req, resp):
        num = req.get_param_as_int("num", default=3)
        delay = req.get_param_as_float("delay", default=1.0)
        multi_sleep(num, delay)
        falcon_util.get_falcon_resp(resp)
