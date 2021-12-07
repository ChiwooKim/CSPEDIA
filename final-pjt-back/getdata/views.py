from rest_framework.response import Response
from movies.serializers import MovieSerializer, GenreSerializer
import requests
from rest_framework.decorators import api_view
import datetime


API_KEY = 'bdbe567df74cea67764cbe196e5d5ae6'

# 특정 영화의 국가를 리턴하는 함수
def get_country(movie_id):
    API_URL = 'https://api.themoviedb.org/3/movie/'
    response = requests.get(f'{API_URL}/{movie_id}?api_key={API_KEY}&language=ko-kr')
    data = response.json()
    try:
        country = data['production_countries'][0]['name']
    except:
        return False
    return country


# 특정 영화의 credit 데이터를 리턴하는 함수
def get_credit(movie_id):
    API_URL = f'https://api.themoviedb.org/3/movie/{movie_id}/credits'
    response = requests.get(f'{API_URL}?api_key={API_KEY}&language=ko-kr')

    actors = ''
    for i in range(4):
        try:
            actors += response.json()['cast'][i]['name']
            if i < 3:
                actors += ', '
        except:
            actors += ''
    
    crews = response.json()['crew']
    for person in crews:
        if person['job'] == 'Director':
            director = person['name']

    return (actors, director)

# 특정 영화의 video key 를 리턴하는 함수
def get_video_key(movie_id):
    API_URL = 'https://api.themoviedb.org/3/movie/'
    response = requests.get(f'{API_URL}/{movie_id}/videos?api_key={API_KEY}&language=ko-kr')
    data = response.json()
    try:
        video_key = data['results'][0]['key']
    except:
        return False
    return video_key


@api_view(['GET'])
def movie_data(request):
    API_URL = 'https://api.themoviedb.org/3/movie/popular'
    data = []

    for page_num in range(11, 13):
        response = requests.get(f'{API_URL}?api_key={API_KEY}&language=ko-kr&page={page_num}')
        movies = response.json()['results']
        print(movies)

        for movie in movies:
            # 줄거리, country, video_path 없는 영화는 pass
            if not movie['overview'] or not get_video_key((movie['id'])) or not get_country((movie['id'])):
                continue
            
            # test genre
            print(movie['genre_ids'])

            # 영화의 감독, 출연진 정보 빼오기
            actors, director = get_credit(movie['id'])

            movie_data = {
                # 기본 필드
                'id': movie['id'],
                'title': movie['title'],
                'overview': movie['overview'],
                'release_date': datetime.datetime.strptime(movie['release_date'], '%Y-%m-%d'),
                'poster_path': movie['poster_path'],
                'backdrop_path': movie['backdrop_path'],
                'vote_count': movie['vote_count'],
                'vote_average': movie['vote_average'],
                'popularity': int(movie['popularity']),

                # 추가 필드
                'country': get_country(movie['id']),
                'actors': actors,
                'director': director,
                'video_key': get_video_key(movie['id']),
                'genres': movie['genre_ids'],
            }
            
            data.append(movie_data)
            print(movie_data)

    
    print('영화데이터 개수: ', len(data))

    serializer = MovieSerializer(data=data, many=True)

    if serializer.is_valid(raise_exception=True):
        # DB에 data 저장
        serializer.save()
        return Response(serializer.data)     


# 장르 데이터 가져와 DB에 넣기
@api_view(['GET'])
def genre_data(request):
    API_URL = 'https://api.themoviedb.org/3/genre/movie/list'
    response = requests.get(f'{API_URL}?api_key={API_KEY}&language=ko-kr')

    data = response.json()['genres']
    serializer = GenreSerializer(data=data, many=True)

    if serializer.is_valid(raise_exception=True):
        # DB에 data 저장
        serializer.save()
        return Response(serializer.data)





from django.contrib.auth import get_user_model
from django_seed import Seed
from faker import Faker
from movies.models import Movie
from community.models import Comment, Review
import random


def testdata(request):
    fake = Faker()
    seeder = Seed.seeder()
    print('check1')
    # for i in range(200):
    #     get_user_model().objects.create(
    #         username = fake.name(),
    #         email = fake.email(),
    #         password = seeder.faker.password(),
    #     )
    print('check2')
    print(get_user_model().objects.all())
    for i in range(300):
        Review.objects.create(
            title = fake.sentence(),
            content = fake.text(),
            rank = random.choice(range(1,11)),
            movie = random.choice(Movie.objects.all()),
            user = random.choice(get_user_model().objects.all()),
        )
    print('check3')
    for i in range(400):
        Comment.objects.create(
            user = random.choice(get_user_model().objects.all()),
            review = random.choice(Review.objects.all()),
            content = '{}번째 content'.format(i),
        )
    print('check4')
