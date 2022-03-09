from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from .models import User
from django.contrib.auth import authenticate

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('name','email', 'id', 'is_admin', 'is_staff')
        extra_kwargs = {
            'id': {'read_only':True},
            'is_admin': {'read_only':True},
            'is_staff': {'read_only':True}
        }

#Register Serializer
class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
            required=True,
            validators=[UniqueValidator(queryset=User.objects.all())]
            )

    class Meta:
        model = User
        fields = ('name', 'email', 'password', 'id', 'is_admin', 'is_staff')
        extra_kwargs = {
            'password': {'write_only':True},
            'id': {'read_only':True},
            'is_admin': {'read_only':True},
            'is_staff': {'read_only':True}
        }


    def create(self, validated_data):
        user = User.objects.create_user(
            validated_data['email'],
            validated_data['password'],
        )
        user.name = validated_data['name']
        user.save()
        return user

        
#Login Serializer
class LoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Incorrect Credentials")