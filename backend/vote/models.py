from tkinter import CASCADE
from django.db import models
from user.models import User
from movie.models import Movie

class Vote(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)