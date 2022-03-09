"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import include, path
from movie.views import MovieDetails
import movie.views as MovieView
import vote.views as VoteView

urlpatterns = [
    path('<int:movie_id>/', MovieDetails.as_view()),
    path('<int:movie_id>/reviews/', include('review.urls')),
    path('<int:movie_id>/upvote/', VoteView.upVote),
    path('<int:movie_id>/downvote/', VoteView.downVote),
    path('<int:movie_id>/watched/', MovieView.watched),
]