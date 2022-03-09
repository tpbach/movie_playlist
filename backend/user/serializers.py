from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
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
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only':True},
            'id': {'read_only':True},
            'is_admin': {'read_only':True},
            'is_staff': {'read_only':True}
        }


    def create(self, validated_data):
        user = User.objects.create_user(
            validated_data['username'],
            validated_data['password'],
        )
        user.save()
        return user
