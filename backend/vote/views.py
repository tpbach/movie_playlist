
from vote.serializers import VoteSerializer
from movie.serializers import MovieSerializer
from movie.models import Movie
from .models import Vote
from user.models import User
from django.http import HttpResponse, HttpResponseRedirect
from rest_framework.views import APIView
from django.contrib.auth.decorators import login_required
from rest_framework.response import Response
from django.contrib.auth.mixins import LoginRequiredMixin


class VoteList(LoginRequiredMixin, APIView):
    def get(self, request):
        try:
            user = User.objects.get(pk=request.user.id)
            votes = Vote.objects.filter(creator=user)
            serializer = VoteSerializer(votes, many=True)
            return Response(serializer.data, status=200)
        except User.DoesNotExist and Vote.DoesNotExist:
            return HttpResponse("Bad Request", status=400)

@login_required
def upVote(request, movie_id):
    user = User.objects.get(pk=request.user.id)
    current_votes = Vote.objects.filter(creator=user)
    if len(current_votes) < 10:
        try:
            movie = Movie.objects.get(pk=movie_id)
            if movie.watched:
                return HttpResponseRedirect('', status=400)
            
            movieData = {
                "votes": str(movie.votes + 1)
            }

            voteData = {
                "creator":user.id,
                "movie" : movie.id
            }

            voteSerializer = VoteSerializer(data=voteData)
            movieSerializer = MovieSerializer(movie, data=movieData, partial=True)
            if voteSerializer.is_valid() and movieSerializer.is_valid():
                voteSerializer.save()
                movieSerializer.save()
                return HttpResponseRedirect('', status=201)
            else:
                return HttpResponseRedirect('', status=400)

        except Movie.DoesNotExist:
            return HttpResponseRedirect('', status=404)
    else:
        return HttpResponseRedirect('', status=403)

@login_required
def downVote(request, movie_id):
    user = User.objects.get(pk=request.user.id)
    movie = Movie.objects.get(pk=movie_id)
    current_votes = Vote.objects.filter(creator=user).filter(movie=movie)
    if len(current_votes) > 0:
        try:
            movie = Movie.objects.get(pk=movie_id)
            if movie.watched:
                return HttpResponseRedirect('', status=400)
                
            vote = current_votes[0]
            
            updatedData = {
                "votes": str(movie.votes - 1)
            }

            serializer = MovieSerializer(movie, data=updatedData, partial=True)
            if serializer.is_valid():
                vote.delete()
                serializer.save()
                return HttpResponseRedirect('', status=201)
            else:
                return HttpResponseRedirect('', status=400)
        except Movie.DoesNotExist:
            return HttpResponseRedirect('', status=404)
    else:
        return HttpResponseRedirect('', status=400)
