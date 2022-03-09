from django.db import models
from django.conf import settings
from django.utils import timezone

class Movie(models.Model):
    title = models.CharField(max_length=200)
    imdb = models.URLField(blank=True)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)
    ratingCount = models.IntegerField(default=0)
    date_added = models.DateTimeField(default = timezone.now)

    watched = models.BooleanField(default=False)
    date_watched = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.title