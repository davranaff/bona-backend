def templateForResponse(data=None, status=None, error=None):
    return {
        "data": data,
        "status": status,
        "error": error
    }
