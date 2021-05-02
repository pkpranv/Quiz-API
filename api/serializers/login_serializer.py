from django.contrib.auth import authenticate
from rest_framework import serializers

class LoginViewSerializer(serializers.Serializer):
    email = serializers.CharField(label=("Email"))
    password = serializers.CharField(label=("Password"),
                                     style={'input_type': 'password'})

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')
        user = authenticate(email=email, password=password)
        if not user:
            raise serializers.ValidationError("User name or password incorrect")
        self.context['request'].user = user
        return True