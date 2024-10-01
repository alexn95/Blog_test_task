from django.db.models import F
from django.utils.decorators import method_decorator
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from core.filters import PostsFilterSet
from core.models import Post, User, Tag, Comment
from core.seriallizers import PostSerializer, UserSerializer, TagSerializer, CommentSerializer, \
    LikesUpdateSerializer

post_param = [
    openapi.Parameter(name='author_id', in_='query', type=openapi.TYPE_INTEGER),
    openapi.Parameter(name='likes_gt', in_='query', type=openapi.TYPE_INTEGER),
    openapi.Parameter(name='tag', in_='query', type=openapi.TYPE_INTEGER),
    openapi.Parameter(name='only_last_month', in_='query', type=openapi.TYPE_BOOLEAN)
]


@method_decorator(name='list', decorator=swagger_auto_schema(manual_parameters=post_param))
class PostViewSet(ModelViewSet):
    queryset = Post.objects.with_comments_count().order_by('-published_at')
    serializer_class = PostSerializer
    filterset_class = PostsFilterSet
    filter_backends = (DjangoFilterBackend,)


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class TagViewSet(ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class BestPostsView(GenericAPIView):
    queryset = Post.objects.with_comments_count()
    serializer_class = PostSerializer

    def get_queryset(self):
        return self.queryset.order_by('-comments_count')[:5]

    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class LikesIncreaseView(GenericAPIView):
    queryset = Post.objects.all()
    serializer_class = LikesUpdateSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        Post.objects.filter(
            pk__in=serializer.data['posts']
        ).update(likes=F('likes') + serializer.data['likes_count'])

        return Response(status=status.HTTP_200_OK)
