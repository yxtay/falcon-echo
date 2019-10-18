from src.util.logger import logger
from src.util.tracer import start_trace_span, trace_function


class Request(object):
    @trace_function
    def __init__(self):
        self.attributes = {}
        self.error = False

    @classmethod
    @trace_function
    def from_falcon_req(cls, req):
        self = cls()
        self.set_attributes(req)
        self.error = self.is_error_req(req)

        if self.error:
            raise ValueError("test")
        return self

    @trace_function
    def is_error_req(self, req):
        return req.get_param_as_bool("error") or (req.media and req.media.get("error"))

    @trace_function
    def set_attributes(self, req):
        self.attributes = {
            "uri": req.uri,
            "method": req.method,
            "headers": req.headers,
            "params": req.params,
            "body": req.media or {}
        }

        with start_trace_span("[logger.info]"):
            logger.info("request attributes", extra={"attributes": self.attributes})
        return self
