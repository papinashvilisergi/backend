from rest_framework.generics import CreateAPIView
from .serializers import RegisterUserSerializer
from rest_framework.exceptions import ValidationError


class RegisterPage(CreateAPIView):
    serializer_class = RegisterUserSerializer

    def create(self, request, *args, **kwargs):
        # Check if fullname is in the request data
        if 'fullname' not in request.data or not request.data.get('fullname').strip():
            raise ValidationError({"fullname": "This field is required."})
        return super().create(request, *args, **kwargs)
