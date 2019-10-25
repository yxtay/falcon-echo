import json

import falcon

from src.request import Request
from src.util import falcon as falcon_util
from src.util.tracer import init_tracer


class HealthResource(object):
    def on_get(self, req, resp):
        body = {
            "status": falcon.HTTP_200,
        }
        resp.body = json.dumps(body)


class HelloResource(object):
    def on_get(self, req, resp):
        tracer = init_tracer()
        with tracer.span(req.uri):
            falcon_util.get_falcon_resp(resp, {"message": "hello"})
        tracer.finish()


class EchoResource(object):
    @falcon_util.add_exception_handling
    def on_get(self, req, resp):
        tracer = init_tracer()
        with tracer.span(req.uri):
            request = Request.from_falcon_req(req)
            falcon_util.get_falcon_resp(resp, request.attributes)

        tracer.finish()

    @falcon_util.add_exception_handling
    def on_post(self, req, resp):
        tracer = init_tracer()
        with tracer.span(req.uri):
            request = Request.from_falcon_req(req)
            falcon_util.get_falcon_resp(resp, request.attributes)

        tracer.finish()
