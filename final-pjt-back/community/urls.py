from django.urls import path
from . import views

urlpatterns = [
    path('<int:movie_id>/',views.index),
    # 영화 detail에(id) 리뷰를 작성
    path('<int:movie_id>/create/', views.create_review),
    # 리뷰 detail & update & delete
    path('<int:review_pk>/reviews/', views.review_detail_update_delete),
    # 리뷰에 대응하는 댓글 목록 & 생성
    path('<int:review_pk>/comments/', views.comment_list_create),
    # 리뷰 좋아요
    path('<int:review_pk>/review_like/', views.review_like),
    # 댓글 삭제
    path('<int:comment_pk>/comments/delete/', views.comment_delete),
    # 특정 user가 작성한 리뷰 반환 (paginator)
    path('<int:user_id>/user_reviews/', views.user_reviews),
    # 특정 user가 작성한 모든 반환
    path('<int:user_id>/user_reviews_all/', views.user_reviews_all)
]
