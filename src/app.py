from wsgiref import simple_server

import falcon

from src import resource
from src.util.misc import get_error_resp


def create_falcon_app():
    app = falcon.API()
    app.add_error_handler(Exception, get_error_resp)

    app.add_route("/", resource.HealthResource())
    app.add_route("/health", resource.HealthResource())
    app.add_route("/hello", resource.HelloResource())
    app.add_route("/echo", resource.EchoResource())
    app.add_route("/auth_echo", resource.EchoResource())
    return app


app = create_falcon_app()

if __name__ == "__main__":
    httpd = simple_server.make_server("127.0.0.1", 8080, app)
    httpd.serve_forever()
