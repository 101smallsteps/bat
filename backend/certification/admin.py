from django.contrib import admin

# Register your models here.
from .models import Course,Quiz,Question,Answer,UserAttempt
from django.contrib.auth.models import User



@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    fields = (
        "title","description"
    )
    list_display = (
        "title","description"
    )

@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    fields = (
        "course","title","description","total_questions"
    )
    list_display = (
        "course","title","description","total_questions"
    )


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    fields = (
        "quiz","question_text"
    )
    list_display = (
        "quiz","question_text"
    )

@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    fields = (
        "question","answer_text","is_correct"
    )
    list_display = (
        "question","answer_text","is_correct"
    )


@admin.register(UserAttempt)
class UserAttemptAdmin(admin.ModelAdmin):
    fields = (
        "user","quiz","current_question","score","completed"
    )
    list_display = (
        "user","quiz","current_question","score","completed"
    )

