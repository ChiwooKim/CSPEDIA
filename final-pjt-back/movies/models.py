from django.db import models
from django.conf import settings


class Genre(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Movie(models.Model):
    # 기본 필드
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=100)
    overview = models.TextField()
    release_date = models.DateTimeField()
    poster_path = models.CharField(max_length=200)
    backdrop_path = models.CharField(max_length=200)
    vote_count = models.IntegerField()
    vote_average = models.FloatField()
    popularity = models.IntegerField()
    # 추가 필드
    country = models.CharField(max_length=100)
    actors = models.CharField(max_length=200)
    director = models.CharField(max_length=200)
    video_key = models.CharField(max_length=200)
    genres = models.ManyToManyField(Genre)
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='like_movies')

    def __str__(self):
        return self.title



