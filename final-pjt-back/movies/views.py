from django.shortcuts import get_object_or_404
from django.http.response import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import GenreSerializer, MovieSerializer
from .models import Movie, Genre



@api_view(['GET'])
def index(request):
    popularity_movies = Movie.objects.order_by('-popularity')[:20]
    latest_movies = Movie.objects.order_by('-release_date')[:20]
    vote_movies = Movie.objects.order_by('-vote_average')[:20]

    popularity_serializer = MovieSerializer(popularity_movies, many=True)
    latest_serializer = MovieSerializer(latest_movies, many=True)
    vote_serializer = MovieSerializer(vote_movies, many=True)

    context = {
        'popularity_movies' : popularity_serializer.data,
        'latest_movies' : latest_serializer.data,
        'vote_movies' : vote_serializer.data,
    }

    return Response(context)


@api_view(['GET'])
def detail(request, movie_pk):
    # pk = movie.id
    movie = get_object_or_404(Movie, pk=movie_pk)
    serializer = MovieSerializer(movie)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def movie_like(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    user = request.user

    if movie.like_users.filter(pk=user.pk).exists():
        movie.like_users.remove(user)
        liked = False
    else:
        movie.like_users.add(user)
        liked = True

    context = {
        'liked' : liked,
    }
    return JsonResponse(context)



@api_view(['GET'])
def get_movie(request):
    movies = Movie.objects.all()

    serializer = MovieSerializer(movies, many=True)

    return Response(serializer.data)

@api_view(['GET'])
def get_genre(request):
    genre = Genre.objects.all()

    serializer = GenreSerializer(genre, many=True)

    return Response(serializer.data)