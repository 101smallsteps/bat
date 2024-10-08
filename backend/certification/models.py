# quiz/models.py

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import uuid  # For generating a unique ID
class Course(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()

class CertificateType(models.Model):
    id = models.AutoField(primary_key=True)  # Auto-generated ID
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Quiz(models.Model):
    course = models.ForeignKey(Course, related_name="quizzes", on_delete=models.CASCADE)
    certificate_type = models.ForeignKey(CertificateType, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(default="Default description")
    total_questions = models.IntegerField()

#class Question(models.Model):
#    quiz = models.ForeignKey(Quiz, related_name="questions", on_delete=models.CASCADE)
#    question_text = models.CharField(max_length=255)
#    correct_answer = models.CharField(max_length=255)

class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    question_text = models.CharField(max_length=500)

    def __str__(self):
        return self.question_text


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    answer_text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.answer_text

class UserAttempt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    current_question = models.ForeignKey(Question, null=True, on_delete=models.SET_NULL)
    score = models.FloatField(default=0.0)
    completed = models.BooleanField(default=False)
    started_at = models.DateTimeField(auto_now_add=True)  # New field
    completed_at = models.DateTimeField(null=True, blank=True)  # New field
    certification_granted = models.BooleanField(default=False)
class SubmittedAnswer(models.Model):
    attempt = models.ForeignKey(UserAttempt, on_delete=models.CASCADE, related_name='submitted_answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    class Meta:
        unique_together = ('attempt', 'question')  # Ensures one answer per question per attempt

class Certificate(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    score = models.FloatField()
    generated_on = models.DateTimeField(auto_now_add=True)
    attempt = models.OneToOneField(UserAttempt, on_delete=models.CASCADE)  # New field
    file_path = models.CharField(max_length=255)


