import json

import falcon

from src.request import Request
from src.util.misc import get_error_resp, get_falcon_resp
from src.util.tracer import init_tracer


class HealthResource(object):
    def on_get(self, req, resp):
        body = {
            "status": falcon.HTTP_200,
            "status_code": 200,
            "message": "ok",
        }
        resp.body = json.dumps(body)


class HelloResource(object):
    def on_get(self, req, resp):
        tracer = init_tracer()
        with tracer.span(req.uri):
            get_falcon_resp(resp, {"message": "hello"})
        tracer.finish()


class EchoResource(object):
    def on_get(self, req, resp):
        tracer = init_tracer()
        with tracer.span(req.uri):
            try:
                request = Request.from_falcon_req(req)
                get_falcon_resp(resp, request.attributes)

            except Exception as e:
                get_error_resp(resp, e)

        tracer.finish()

    def on_post(self, req, resp):
        tracer = init_tracer()
        with tracer.span(req.uri):
            try:
                request = Request.from_falcon_req(req)
                get_falcon_resp(resp, request.req_attributes)

            except Exception as e:
                get_error_resp(resp, e)

        tracer.finish()
