from app.errors import Error


class ApplicationError(Exception):
    def __init__(self, status_code: int, body: Error | None = None, headers: dict[str, str] | None = None):
        self.status_code = status_code
        self.body = body
        self.headers = headers
