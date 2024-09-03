from app.models import Model
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse


def create_response(status_code: int, body: Model | list[Model] | None = None, headers: dict[str, str] | None = None):
    return JSONResponse(status_code=status_code, content=jsonable_encoder(body), headers=headers)
