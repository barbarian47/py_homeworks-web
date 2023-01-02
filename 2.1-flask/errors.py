from flask import Flask, jsonify


app = Flask('app')


class HttpError(Exception):

    def __init__(self, status_code: int, message: str | dict | list):
        self.status_sode = status_code
        self.message = message


@app.errorhandler(HttpError)
def http_error_handler(err: HttpError):
    response = jsonify({
        'status': 'error',
        'message': err.message,
    })
    response.status_code = err.status_sode
    return response
