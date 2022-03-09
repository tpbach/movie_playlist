from rest_framework.views import APIView
from django.http import HttpResponse
from rest_framework.response import Response
from movie.models import Movie
from .models import Review
from .serializers import ReviewSerializer
from movie.serializers import MovieSerializer
from statistics import mean

# Create your views here.
class MovieReviews(APIView):
    
    def get(self, request, movie_id):
        movie = Movie.objects.get(pk=movie_id)
        reviews = Review.objects.filter(movie=movie)
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data, status=200)
    
    def post(self, request, movie_id):
        request_data = request.data
        userRating = int(request_data["rating"])

        reviewSerializer = ReviewSerializer(data=request_data)
        if reviewSerializer.is_valid():

            # Get the movie and all it's reviews
            movie = Movie.objects.get(pk=movie_id)
            all_reviews = Review.objects.filter(movie=movie).values("rating")
            ratings = []

            # Get sum of all ratings
            if len(all_reviews) > 0:
                for review in all_reviews:
                    ratings.append(review["rating"])
            ratings.append(int(request_data["rating"]))

            newRating = int(mean(ratings))

            # Update movie
            updatedData = {
                "rating" : str(newRating),
                "ratingCount" : str(movie.ratingCount+1)
            }
            
            movieSerializer = MovieSerializer(movie, data=updatedData, partial=True)
            
            if movieSerializer.is_valid():
                # Save movie and review
                movieSerializer.save()
                reviewSerializer.save()
                return Response(reviewSerializer.data, status=201)
        else:
            return Response(reviewSerializer.errors, status=400)

class ReviewDetails(APIView):
    def get(self, request, movie_id, review_id):
        try:
            review = Review.objects.get(pk=review_id)
            serializer = ReviewSerializer(review)
            print(serializer.data)
            return Response(serializer.data, status=200)
        except Review.DoesNotExist:
            return HttpResponse("Review does not exists.", status=404)

    def put(self, request, movie_id, review_id):
        try:
            review = Review.objects.get(pk=review_id)

            reviewSerializer = ReviewSerializer(review, data=request.data, partial=True)
            if reviewSerializer.is_valid():
                reviewSerializer.save()
                 # Update movie rating
                movie = Movie.objects.get(pk=movie_id)
                all_reviews = Review.objects.filter(movie=movie).values("rating")
                ratings = []

                # Get sum of all ratings
                if len(all_reviews) > 0:
                    for review in all_reviews:
                        ratings.append(review["rating"])
                
                newRating = int(mean(ratings))
                
                # Update movie
                updatedData = {
                    "rating" : str(newRating),
                    "ratingCount" : str(movie.ratingCount+1)
                }
                
                movieSerializer = MovieSerializer(movie, data=updatedData, partial=True)
                
                if movieSerializer.is_valid():
                    # Save movie and review
                    movieSerializer.save()
                    return Response(reviewSerializer.data, status=200)
            else:
              return Response(reviewSerializer.errors, status=400)  
           
        except Review.DoesNotExist:
            return HttpResponse("Review does not exists.", status=404)

    def delete(self, request, movie_id, review_id):
        try:
            review = Review.objects.get(pk=review_id)
            review.delete()

            # Update movie rating
            movie = Movie.objects.get(pk=movie_id)
            all_reviews = Review.objects.filter(movie=movie).values("rating")
            ratings = []

            # Get sum of all ratings
            if len(all_reviews) > 0:
                for review in all_reviews:
                    ratings.append(review["rating"])
            
            newRating = int(mean(ratings))
            
            # Update movie
            updatedData = {
                "rating" : str(newRating),
                "ratingCount" : str(movie.ratingCount-1)
            }
            
            movieSerializer = MovieSerializer(movie, data=updatedData, partial=True)
            
            if movieSerializer.is_valid():
                # Save movie and review
                movieSerializer.save()
            return HttpResponse("Successfully deleted the review.", status=201)
        except Review.DoesNotExist:
            return HttpResponse("Review does not exists.", status=404)

            