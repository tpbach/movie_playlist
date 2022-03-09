from rest_framework.views import APIView
from django.http import HttpResponse
from rest_framework.response import Response
from movie.models import Movie
from review.models import Review
from .serializers import MovieSerializer
import json

# Create your views here.
class MovieList(APIView):
    """Movie List"""

    # Get all movies in the list
    def get(self, request):
        all_movies = Movie.objects.all().order_by("-date_added")

        serializer = MovieSerializer(all_movies, many=True)
        return Response(serializer.data, status=200)
    
    # Add a movie to the list
    def post(self, request):
        request_data = request.data.copy()
        serializer = MovieSerializer(data=request_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        else:
            return Response(serializer.errors, status=400)

class MovieDetails(APIView):
    """ Movie Details """
    def get(self, request, movie_id):
        try:
            movie = Movie.objects.get(pk=movie_id)
            serializer = MovieSerializer(movie, context={'request': request})
             
            return Response(serializer.data, status=200)
        except Movie.DoesNotExist:
            return HttpResponse("Movie does not exists", status=404)
    
    def put(self, request, movie_id):
        try:
            movie = Movie.objects.get(pk=movie_id)
            serializer = MovieSerializer(movie, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=200)
            else:
              return Response(serializer.errors, status=400)  
        except Movie.DoesNotExist:
            return HttpResponse("Movie does not exists", status=404)
    
    def delete(self, request, movie_id):
        try:
            movie = Movie.objects.get(pk=movie_id)
            movie.delete()
            return HttpResponse("Successfully deleted the movie.", status=201)
        except  Movie.DoesNotExist:
            return HttpResponse("Movie not found.", status=404) 