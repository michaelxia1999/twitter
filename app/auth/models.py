from app.models import Model


class UserCredentials(Model):
    username: str
    password: str


class Session(Model):
    id: str
