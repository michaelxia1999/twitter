from app.errors import Error
from fastapi import FastAPI
from typing import Any


def generate_responses(input: bool, auth: bool, responses: list[tuple[int, Any]]) -> dict:
    responses.append((500, None))

    if input:
        responses.append((400, Error))

    if auth:
        responses.append((401, None))

    generated_responses = {}

    for code, model in responses:
        if not model:
            generated_responses[code] = {"content": {"application/json": {"schema": {}}}}

        else:
            generated_responses[code] = {"model": model}

        if code == 200:
            generated_responses[code]["description"] = "OK"

    return generated_responses


def configure_schema(app: FastAPI):
    schema = app.openapi()

    for path in schema["paths"].values():
        for method in path.values():
            keys_to_delete = []

            for status_code in method["responses"]:
                if status_code == "200" and method["responses"]["200"]["description"] == "Successful Response":
                    keys_to_delete.append(status_code)

                if status_code == "422":
                    keys_to_delete.append(status_code)

            for status_code in keys_to_delete:
                method["responses"].pop(status_code)

    app.openapi_schema = schema
