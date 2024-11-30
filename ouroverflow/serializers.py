from rest_framework import serializers
from .models import Question, Answer, Tag
from user.serializers import UserSerializer


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']


class AnswerSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    likes = UserSerializer(many=True, read_only=True)  # Show who liked the answer
    likes_count = serializers.SerializerMethodField()

    class Meta:
        model = Answer
        fields = ['id', 'text', 'author', 'likes', 'likes_count', 'is_correct', 'created_at']

    def get_likes_count(self, obj):
        return obj.likes.count()


class QuestionSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    answers_count = serializers.IntegerField(source='answers.count', read_only=True)
    tags = TagSerializer(many=True)  # Use the TagSerializer to represent tags

    class Meta:
        model = Question
        fields = ['id', 'title', 'description', 'tags', 'author', 'answers_count', 'created_at']
