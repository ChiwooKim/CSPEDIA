from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import UserSerializer
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from django.http.response import JsonResponse
from community.models import Review


@api_view(['POST'])
def signup(request):
    password = request.data.get('password')
    password_confirmation = request.data.get('password_confirmation')

    if password != password_confirmation:
        return Response({
            'password': ['비밀번호가 일치하지 않습니다']
        }, status=status.HTTP_400_BAD_REQUEST)
        
    serializer = UserSerializer(data=request.data)

    if serializer.is_valid(raise_exception=True):
        user = serializer.save()
        user.set_password(password)
        user.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
# @permission_classes([IsAuthenticated])
def profile(request, user_id):
    person = get_object_or_404(get_user_model(), pk=user_id)
    reviews = Review.objects.filter(user=user_id)

    context = {
        'username': person.username,
        'email': person.email,
        'like_movies': list(person.like_movies.all().values()),
        'like_reviews': list(person.like_reviews.all().values()),
        'reviews': list(reviews.values())
    }
    
    return JsonResponse(context)