from app.database.postgres.core import create_tables, drop_tables, engine
from app.database.redis.core import redis
from app.exc.core import ApplicationError
from app.exc.handlers import application_error_handler, http_error_handler, request_validation_error_handler, response_validation_error_handler, validation_error_handler
from app.middlewares import server_error_middleware
from app.notification.orm import Notification
from app.openapi import configure_schema
from app.router import router
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError, ResponseValidationError
from pydantic import ValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()
    yield
    await drop_tables()
    await engine.dispose()
    await redis.flushdb()
    await redis.close()


app = FastAPI(lifespan=lifespan)


app.middleware("http")(server_error_middleware)

app.exception_handler(RequestValidationError)(request_validation_error_handler)
app.exception_handler(ResponseValidationError)(response_validation_error_handler)
app.exception_handler(ValidationError)(validation_error_handler)
app.exception_handler(ApplicationError)(application_error_handler)
app.exception_handler(StarletteHTTPException)(http_error_handler)

app.include_router(router=router)


configure_schema(app=app)
