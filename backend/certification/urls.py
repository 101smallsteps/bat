from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import QuizDetailView, StartQuizView, SubmitAnswerView, QuizViewSet, QuestionViewSet, QuizStatusView,UserAttemptsView,GenerateCertificateView,download_certificate

router = DefaultRouter()
router.register('quizzes', QuizViewSet)
router.register('questions', QuestionViewSet)

urlpatterns = [
    path('quiz/<int:quiz_id>/', QuizDetailView.as_view(), name='quiz-detail'),
    path('quiz/<int:quiz_id>/start/', StartQuizView.as_view(), name='start-quiz'),
    path('quiz/<int:quiz_id>/question/<int:question_id>/submit/', SubmitAnswerView.as_view(), name='submit-answer'),
    path('quiz-status/', QuizStatusView.as_view(), name='quiz-status'),
    path('attempts/', UserAttemptsView.as_view(), name='attempts'),
    path('quiz/<int:quiz_id>/generate_certificate/', GenerateCertificateView.as_view(),name='generate_certificate'),
    path('certificates/download/<str:file_name>/', download_certificate, name='download_certificate'),
    path('', include(router.urls)),
]
