from rest_framework import serializers
from .models import Quiz, Question, Answer, UserAttempt, SubmittedAnswer, Certificate

class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['id', 'answer_text']

class QuestionSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True)

    class Meta:
        model = Question
        fields = ['id', 'question_text', 'answers']

class QuizSerializer(serializers.ModelSerializer):
    questions = serializers.SerializerMethodField()

    class Meta:
        model = Quiz
        fields = ['id', 'title', 'total_questions', 'questions']

    def get_questions(self, obj):
        # Only return the count of questions instead of full data
        return obj.questions.count()

class UserAttemptSerializer(serializers.ModelSerializer):
    quiz_title = serializers.CharField(source='quiz.title')

    class Meta:
        model = UserAttempt
        fields = ['id', 'quiz_title', 'score', 'completed_at', 'certification_granted']

class CertificateSerializer(serializers.ModelSerializer):
    quiz_title = serializers.CharField(source='quiz.title', read_only=True)

    class Meta:
        model = Certificate
        fields = ['id', 'quiz_title', 'score', 'generated_on']