from django.db import models
from django.conf import settings
from movies.models import Movie
from django.core.validators import MaxValueValidator, MinValueValidator

class Review(models.Model):
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL,related_name='like_reviews', blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete = models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    rank = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(10)])
   

class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    review = models.ForeignKey(Review, on_delete=models.CASCADE)
    content = models.CharField(max_length=300)
