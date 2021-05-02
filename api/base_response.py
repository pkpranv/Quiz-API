from rest_framework import status
from rest_framework.response import Response
from .error_codes import get_error_code


class HttpSuccessResponse(Response):
    def __init__(self, data, message=None, **kwargs):
        data = {
            "status": 'OK',
            "message": message if message else "",
            "data": data if data else []
        }
        super(HttpSuccessResponse, self).__init__(data, **kwargs)


class HttpErrorResponse(Response):
    def __init__(self, message, data=None, status_code=None, **kwargs):
        data = {"status": 'error', "message": message, "error_data": data}
        error_code = kwargs.get('error_code', None)
        if error_code:
            kwargs.pop('error_code')
            data['error_code'] = error_code
        elif 'error_code' in kwargs:
            kwargs.pop('error_code')
        if 'status' in kwargs:
            status_code = kwargs['status']
        self.status_code = status_code if status_code else 400
        super(HttpErrorResponse, self).__init__(data, **kwargs)
