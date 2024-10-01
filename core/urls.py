from django.urls import path, include
from rest_framework import routers

from core import views

router = routers.DefaultRouter()
router.register('posts', views.PostViewSet)
router.register('tags', views.TagViewSet)
router.register('users', views.UserViewSet)
router.register('comments', views.CommentViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('best_posts/', views.BestPostsView.as_view()),
    path('likes_increase/', views.LikesIncreaseView.as_view()),
]
