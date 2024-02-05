def status(status, body, message, error):
    data = {"status": status, "data": body, "message": message, "error": error}
    return data
