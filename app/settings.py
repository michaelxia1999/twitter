from os import environ

ENV = environ["ENV"]
POSTGRES_URL = environ["POSTGRES_URL"]
REDIS_PWD = environ["REDIS_PWD"]
SESSION_TIMEOUT_SECONDS = int(environ["SESSION_TIMEOUT_SECONDS"])
