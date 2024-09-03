import traceback


def format_validation_error_location(error_location: tuple[int | str, ...]) -> str:
    formatted_error_location = ""

    for path in error_location:
        if isinstance(path, int):
            formatted_error_location += f"[{path}]"
        else:
            if formatted_error_location:
                formatted_error_location += f".{path}"
            else:
                formatted_error_location += path

    return formatted_error_location


def format_traceback(e: Exception) -> list[str]:
    return traceback.format_exception(type(e), e, e.__traceback__)
