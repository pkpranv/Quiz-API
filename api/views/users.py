from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny

from django.conf import settings

from ..base_response import HttpErrorResponse,HttpSuccessResponse
from ..error_codes import get_error_code
from ..utils import get_token

from ..serializers.registration_serializer import EmailRegistrationSerializer
from ..serializers.login_serializer import LoginViewSerializer


class RegistrationView(CreateAPIView):
    serializer_class = EmailRegistrationSerializer
    permission_classes = (AllowAny,)

    def post(self, request, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return HttpSuccessResponse({}, "Registration success")
        kwargs_errors = {'error_code': get_error_code(
            serializer.errors.values())}
        return HttpErrorResponse(serializer.errors, **kwargs_errors)

class LoginView(CreateAPIView):
    serializer_class = LoginViewSerializer
    permission_classes = (AllowAny,)

    def post(self, request, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            token = get_token(request.user)
            return HttpSuccessResponse({'token': token},
                                       "login success")

        kwargs_errors = {'error_code': get_error_code(
            serializer.errors.values())}
        return HttpErrorResponse(serializer.errors, **kwargs_errors)