import falcon


class HTTPValidationError(falcon.HTTPError):
    def __init__(self, errors):
        self.errors = errors
        super().__init__(falcon.HTTP_422)

    def to_dict(self, obj_type=dict):
        pass
