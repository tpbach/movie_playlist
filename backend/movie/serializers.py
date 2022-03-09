from .models import Movie
import requests
from rest_framework.serializers import ModelSerializer, SerializerMethodField

class MovieSerializer(ModelSerializer):
    """Movie Serializer"""
    reviews = SerializerMethodField()

    class Meta:
        model = Movie
        fields = '__all__'

    def get_reviews(self, movie):
        try:
            request = self.context.get('request')
            url_no_id = request.build_absolute_uri().split('/movies/')[0]
            url = url_no_id + '/movies/' + str(movie.id) + '/reviews/'
            response = requests.get(url).json()
            return response
        except:
            return {}