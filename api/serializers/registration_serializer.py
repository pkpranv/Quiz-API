from rest_framework import serializers
from ..models import User

class EmailRegistrationSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        user.save()
        return user

    class Meta:
        model = User
        fields = ( 'email' ,'name', 'password')