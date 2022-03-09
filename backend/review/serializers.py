from .models import Review
from rest_framework.serializers import ModelSerializer

class ReviewSerializer(ModelSerializer):
    """Review Serializer"""
    class Meta:
        model = Review
        fields = '__all__'