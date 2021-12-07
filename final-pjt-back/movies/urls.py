from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('<int:movie_pk>/', views.detail),
    path('<int:movie_pk>/movie_like/', views.movie_like),
    path('getmovie/',views.get_movie),
    path('genre/', views.get_genre),
]
