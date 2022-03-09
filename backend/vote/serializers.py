from .models import Vote
from rest_framework.serializers import ModelSerializer

class VoteSerializer(ModelSerializer):
    """Vote Serializer"""
    class Meta:
        model = Vote
        fields = '__all__'