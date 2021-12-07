from django.urls import path
from. import views

urlpatterns = [
    path('signup/',views.signup),
    path('<int:user_id>/profile/', views.profile),
]
