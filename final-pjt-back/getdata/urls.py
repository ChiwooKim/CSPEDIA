from django.urls import path
from . import views

urlpatterns = [
    path('movie/', views.movie_data),
    path('genre/', views.genre_data),
    path('test/', views.testdata),
]