from app.exc.utils import format_traceback
from app.utils import create_response
from fastapi.requests import Request


# Catches all unhandled exception
async def server_error_middleware(request: Request, call_next):
    try:
        response = await call_next(request)
        return response
    except Exception as e:
        traceback = format_traceback(e=e)
        for trace in traceback:
            print(trace)
        return create_response(status_code=500)
