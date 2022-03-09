from pyexpat import model
from django.db import models
from django.conf import settings
from movie.models import Movie
from django.core.validators import MaxValueValidator, MinValueValidator

class Review(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="review")
    rating = models.IntegerField(default=1, validators=[MaxValueValidator(10), MinValueValidator(1)])
    description = models.TextField(default="I watched this!", max_length=200)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)