from wsgiref import simple_server

import falcon

from src import falcon_resource


def create_falcon_app():
    app = falcon.API()
    app.add_route("/health", falcon_resource.HealthResource())
    app.add_route("/hello", falcon_resource.HelloResource())
    app.add_route("/echo", falcon_resource.EchoResource())
    app.add_route("/auth_echo", falcon_resource.EchoResource())
    return app


app = create_falcon_app()

if __name__ == "__main__":
    httpd = simple_server.make_server("127.0.0.1", 8080, app)
    httpd.serve_forever()
