from django.contrib import admin
from .models import Course, CertificateType, Quiz, Question, Answer, UserAttempt, SubmittedAnswer, Certificate

# Course Admin
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'description')
    search_fields = ('title', 'description')

# Certificate Type Admin
@admin.register(CertificateType)
class CertificateTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)

# Quiz Admin
@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'certificate_type', 'total_questions')
    list_filter = ('course', 'certificate_type')
    search_fields = ('title', 'description')
    autocomplete_fields = ('course', 'certificate_type')  # Enables searching for related fields

# Question Admin
@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question_text', 'quiz')
    list_filter = ('quiz',)
    search_fields = ('question_text',)

# Answer Admin
@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('answer_text', 'question', 'is_correct')
    list_filter = ('is_correct',)
    search_fields = ('answer_text', 'question__question_text')  # Search by answer text and associated question text

# User Attempt Admin
@admin.register(UserAttempt)
class UserAttemptAdmin(admin.ModelAdmin):
    list_display = ('user', 'quiz', 'score', 'completed', 'started_at', 'completed_at', 'certification_granted')
    list_filter = ('completed', 'certification_granted', 'quiz')
    search_fields = ('user__username', 'quiz__title')
    readonly_fields = ('started_at', 'completed_at')

# Submitted Answer Admin
@admin.register(SubmittedAnswer)
class SubmittedAnswerAdmin(admin.ModelAdmin):
    list_display = ('attempt', 'question', 'answer')
    search_fields = ('attempt__user__username', 'question__question_text', 'answer__answer_text')
    list_filter = ('question__quiz',)

# Certificate Admin
@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ('user', 'quiz', 'score', 'generated_on', 'file_path')
    search_fields = ('user__username', 'quiz__title')
    list_filter = ('quiz',)
    readonly_fields = ('generated_on',)
