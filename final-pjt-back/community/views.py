from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator
from django.http.response import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from .serializers import ReviewSerializer, CommentSerializer
from .models import Review, Comment
from movies.models import Movie
from django.db.models import Count


@api_view(['GET'])
def index(request, movie_id):
    # 리뷰가 좋아요가 많은 것이 가장 상단에 올 수 있도록 하고 나머지는 리뷰 생성 순으로 정렬
    reviews = Review.objects.filter(movie=movie_id).annotate(count=Count('like_users')).order_by('-count')
    paginator = Paginator(reviews, 4)
    page_number = request.GET.get('page')

    if int(page_number) > paginator.num_pages:
        return Response()
    page_obj = paginator.get_page(page_number)
    serializer = ReviewSerializer(page_obj, many=True)
    
    return Response(serializer.data)

@api_view(['GET'])
def user_reviews(request, user_id):
    '''
    GET : 특정 유저에 대한 리뷰를 page 별로 응답
    '''
    reviews = Review.objects.filter(user=user_id)
    paginator = Paginator(reviews, 4)
    page_number = request.GET.get('page')

    if int(page_number) > paginator.num_pages:
        return Response()
    page_obj = paginator.get_page(page_number)
    print('페이지 요청', page_number)
    print('page_obj', page_obj)
    print('page_count', paginator.num_pages)
    serializer = ReviewSerializer(page_obj, many=True)
    
    return Response(serializer.data)

@api_view(['GET'])
def user_reviews_all(request, user_id):
    '''
    GET : 특정 유저에 대한 모든 리뷰를 담아 응답
    '''
    reviews = Review.objects.filter(user=user_id)
    serializer = ReviewSerializer(reviews, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_review(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)

    serializer = ReviewSerializer(data=request.data, many=True)
    if serializer.is_valid(raise_exception=True):
        serializer.save(movie=movie, user=request.user)
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def review_detail_update_delete(request, review_pk):
    review = get_object_or_404(Review, pk=review_pk)

    # detail
    if request.method == 'GET':
        serializer = ReviewSerializer(review)
        return Response(serializer.data)

    if request.user.pk == review.user.pk:
        # update
        if request.method == 'PUT':
            serializer = ReviewSerializer(review, data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data)

        # delete 
        elif request.method == 'DELETE':
            review.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
    return Response(status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def comment_list_create(request, review_pk):
    review = get_object_or_404(Review, pk=review_pk)

    if request.method == 'GET':
        comments = review.comment_set.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(review=review, user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def comment_delete(request, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk)
    if request.user.pk == comment.user.pk:
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    return Response(status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def review_like(request, review_pk):
    review = get_object_or_404(Review, pk=review_pk)
    user = request.user

    if review.like_users.filter(pk=user.pk).exists():
        review.like_users.remove(user)
        liked = False
    else:
        review.like_users.add(user)
        liked = True

    context = {
        'liked' : liked,
        'count' : review.like_users.count()
    }
    return JsonResponse(context)
