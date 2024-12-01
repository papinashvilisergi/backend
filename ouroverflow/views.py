from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView, RetrieveAPIView

from .models import Question, Answer
from .serializers import QuestionSerializer, AnswerSerializer
from .permissions import ReadOnlyOrIsAuthenticated, IsQuestionAuthor


class QuestionListCreateView(ListCreateAPIView):
    """
    View to list all questions or create a new question.
    """
    serializer_class = QuestionSerializer
    queryset = Question.objects.all().order_by('-created_at')
    permission_classes = [ReadOnlyOrIsAuthenticated]

    def get_queryset(self):
        tags = self.request.query_params.getlist('tags', [])
        if tags:
            return super().get_queryset().filter(tags__overlap=tags)  # Use `super().get_queryset()` for safety
        return super().get_queryset()  # Ensures `.queryset` is evaluated dynamically

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)



class QuestionDetailView(RetrieveAPIView):
    """
    View to retrieve details of a specific question.
    """
    serializer_class = QuestionSerializer
    queryset = Question.objects.all()
    permission_classes = [ReadOnlyOrIsAuthenticated]


class AnswerListCreateView(ListCreateAPIView):
    """
    View to list or create answers for a specific question.
    """
    serializer_class = AnswerSerializer
    permission_classes = [ReadOnlyOrIsAuthenticated]

    def get_queryset(self):
        question_id = self.kwargs['question_id']
        return Answer.objects.filter(question_id=question_id)

    def perform_create(self, serializer):
        question_id = self.kwargs['question_id']
        serializer.save(author=self.request.user, question_id=question_id)


class LikeAnswerView(APIView):
    """
    View to like an answer.
    """
    permission_classes = [ReadOnlyOrIsAuthenticated]

    def post(self, request, *args, **kwargs):
        answer_id = self.kwargs['answer_id']
        try:
            answer = Answer.objects.get(id=answer_id)
            if request.user in answer.likes.all():
                return Response({"error": "You have already liked this answer."}, status=400)
            answer.likes.add(request.user)
            return Response({"message": "Answer liked successfully."})
        except Answer.DoesNotExist:
            return Response({"error": "Answer not found."}, status=404)


class CorrectAnswerView(APIView):
    """
    View to mark an answer as correct.
    """
    permission_classes = [IsQuestionAuthor]

    def post(self, request, *args, **kwargs):
        answer_id = self.kwargs['answer_id']
        try:
            answer = Answer.objects.get(id=answer_id)

            # Ensure the requesting user is the author of the question
            self.check_object_permissions(request, answer)

            # Unmark any existing correct answers for this question
            Answer.objects.filter(question=answer.question).update(is_correct=False)

            # Mark the selected answer as correct
            answer.is_correct = True
            answer.save()

            return Response({"message": "Marked as correct answer.", "answer_id": answer.id})
        except Answer.DoesNotExist:
            return Response({"error": "Answer not found."}, status=404)
