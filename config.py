import os


def map_level(level):
    return {"critical": 50, "error": 40, "warning": 30, "info": 20, "debug": 10}.get(
        level, 10
    )


LOGGING_LEVEL = map_level(os.environ.get("LOGGING_LEVEL", "debug"))
