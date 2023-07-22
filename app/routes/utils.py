import datetime

from fastapi.responses import JSONResponse


def bad_request(error_text):
    response = {
        "timestamp": str(datetime.datetime.now()),
        "status": 400,
        "error": "Bad Request",
        "message": error_text,
    }
    return JSONResponse(status_code=400, content=response)


def unauthorized():
    response = {
        "timestamp": str(datetime.datetime.now()),
        "status": 401,
        "error": "Unauthorized",
        "message": "You're not authorized",
    }
    return JSONResponse(status_code=401, content=response)


def forbidden():
    response = {
        "timestamp": str(datetime.datetime.now()),
        "status": 403,
        "error": "Forbidden",
        "message": "You're not allowed to access",
    }
    return JSONResponse(status_code=403, content=response)


def not_found(error_text):
    response = {
        "timestamp": str(datetime.datetime.now()),
        "status": 404,
        "error": "Not Found",
        "message": error_text,
    }
    return JSONResponse(status_code=404, content=response)
