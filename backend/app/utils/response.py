def error_response_model(error, code, message):
    return {
        'error': error,
        'code': code,
        'message': message
    }
