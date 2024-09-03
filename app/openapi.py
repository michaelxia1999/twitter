from app.errors import Error
from fastapi import FastAPI
from typing import Any

# For API documentation only


# Add all possible api responses to openapi schema for better api documentation, frontenders are going to love this!
def generate_responses(input: bool, auth: bool, responses: list[tuple[int, Any]]) -> dict:
    # Input means this request takes in user input(body, header, query, path), so 400 with Error is a possible response
    # Auth means this request takes in Session-ID header, so 401 is a possible response
    # Responses take in a list of (status_code, model) that is specific to each api request

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
                # Fastapi automatically generates 200 response for all routes, this is used to remove them.
                if status_code == "200" and method["responses"]["200"]["description"] == "Successful Response":
                    keys_to_delete.append(status_code)

                # Removing this because I believe status code of 400 is more appropriate for client input error.
                if status_code == "422":
                    keys_to_delete.append(status_code)

            for status_code in keys_to_delete:
                method["responses"].pop(status_code)

    app.openapi_schema = schema
