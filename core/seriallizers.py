from rest_framework import serializers

from core.models import Post, User, Tag, Comment


class PostSerializer(serializers.ModelSerializer):
    comments_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Post
        fields = (
            'id',
            'title',
            'content',
            'author',
            'published_at',
            'likes',
            'tags',
            'comments_count'
        )


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('login', 'email', 'created_at', 'password')
        extra_kwargs = {
            'password': {'write_only': True}
        }


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'


class LikesUpdateSerializer(serializers.Serializer):
    likes_count = serializers.IntegerField()
    posts = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all(), many=True)
