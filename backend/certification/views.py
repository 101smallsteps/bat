from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Quiz, Question, Answer, UserAttempt, SubmittedAnswer, Certificate
from .serializers import QuizSerializer, UserAttemptSerializer, QuestionSerializer, CertificateSerializer
from django.contrib.auth.models import User
from rest_framework import generics, permissions
from rest_framework import viewsets
from .serializers import QuizSerializer, QuestionSerializer

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from django.core.files.base import ContentFile
import os

from django.http import FileResponse

def download_certificate(request, file_name):
    permission_classes = [permissions.IsAuthenticated]
    file_path = os.path.join('/usr/src/app/cert_gen/', file_name)
    return FileResponse(open(file_path, 'rb'), as_attachment=True)


class GenerateCertificateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, quiz_id):
        quiz = get_object_or_404(Quiz, id=quiz_id)
        user = request.user

        # Find the latest completed attempt with a passing score
        attempt = UserAttempt.objects.filter(user=user, quiz=quiz, completed=True).order_by('-completed_at').first()

        if not attempt:
            return Response({"error": "No completed quiz attempt found."}, status=404)

        if attempt.score < (0.8 * quiz.questions.count()):
            return Response({"error": "Score is less than 80%. No certificate generated."}, status=400)

        # Check if a certificate already exists
        #certificate, created = Certificate.objects.get_or_create(user=user, quiz=quiz, score=attempt.score)
        certificate = Certificate.objects.filter(user=user, quiz=quiz).order_by('-generated_on').first()

        # Generate PDF certificate
        file_name = self.generate_certificate(user.username, quiz.title, attempt.score)

        # Save the file path in the certificate instance
        certificate.file_path = file_name
        certificate.save()

        return Response({
            "message": "Certificate generated successfully!",
            "certificate_id": certificate.id,
            "file_name": file_name,
            "score": attempt.score
        })

    def generate_certificate(self, username, quiz_title, score):
        # Create PDF
        pdf_file_name = f"{username}_{quiz_title.replace(' ', '_')}_certificate.pdf"
        file_path = os.path.join('/usr/src/app/cert_gen/', pdf_file_name)

        # Create the PDF
        c = canvas.Canvas(file_path, pagesize=letter)
        width, height = letter
        c.drawString(100, height - 100, f"Certificate of Completion")
        c.drawString(100, height - 150, f"This certifies that {username} has successfully completed")
        c.drawString(100, height - 200, f"The quiz: {quiz_title}")
        c.drawString(100, height - 250, f"Score Achieved: {score}")
        c.save()

        return pdf_file_name


# Fetch Quiz Details
class QuizDetailView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, quiz_id):
        quiz = get_object_or_404(Quiz, id=quiz_id)
        serializer = QuizSerializer(quiz)
        return Response(serializer.data)

# Start or resume a quiz attempt
class StartQuizView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, quiz_id):
        quiz = get_object_or_404(Quiz, id=quiz_id)
        user = request.user

        # Check if the user has an unfinished attempt for this quiz
        attempt = UserAttempt.objects.filter(user=user, quiz=quiz, completed=False).first()

        if attempt:
            # Resume the unfinished attempt
            message = "Resuming existing quiz attempt."
        else:
            # Start a new attempt
            first_question = quiz.questions.first()

            if not first_question:
                return Response({"detail": "Quiz has no questions available."}, status=400)

            attempt = UserAttempt.objects.create(user=user, quiz=quiz, current_question=first_question)
            message = "Starting a new quiz attempt."

        # Make sure to include current question in the response
        current_question = attempt.current_question

        if current_question:
            total_questions = quiz.questions.count()
            current_question_index = list(quiz.questions.all()).index(current_question)
        else:
            total_questions = 0
            current_question_index = 0

        # Serialize and return the attempt data along with question details
        serializer = UserAttemptSerializer(attempt)
        return Response({
            "message": message,
            "attempt": {
                "id": attempt.id,
                "score": attempt.score,
                "completed": attempt.completed,
                "total_questions": total_questions,
                "current_question_index": current_question_index,
                "current_question": {
                    "id": current_question.id,
                    "question_text": current_question.question_text,
                    "answers": [
                        {"id": answer.id, "answer_text": answer.answer_text}
                        for answer in current_question.answers.all()
                    ]
                } if current_question else None
            }
        })

class SubmitAnswerView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, quiz_id, question_id):
        user = request.user
        quiz = get_object_or_404(Quiz, id=quiz_id)
        #attempt = get_object_or_404(UserAttempt, user=user, quiz=quiz, completed=False)
        attempt = UserAttempt.objects.filter(user=user, quiz=quiz, completed=False).first()
        question = get_object_or_404(Question, id=question_id)

        submitted_answer_id = request.data.get('answer_id')
        submitted_answer = get_object_or_404(Answer, id=submitted_answer_id)

        # Save the submitted answer
        SubmittedAnswer.objects.create(attempt=attempt, question=question, answer=submitted_answer)

        # Update score if the answer is correct
        if submitted_answer.is_correct:
            attempt.score += 1

        # Fetch the next question in order
        remaining_questions = quiz.questions.filter(id__gt=question.id)
        next_question = remaining_questions.first()

        # Update progress: number of answered questions
        answered_questions_count = SubmittedAnswer.objects.filter(attempt=attempt).count()

        if next_question:
            attempt.current_question = next_question
            attempt.save()

            question_serializer = QuestionSerializer(next_question)
            return Response({
                'next_question': question_serializer.data,
                'progress': f"{answered_questions_count + 1} of {quiz.questions.count()}",
                'score': attempt.score
            })
        else:
            # Quiz is completed
            attempt.completed = True
            attempt.save()

            # Check if certificate should be generated
            passing_score = 0.8 * quiz.questions.count()
            if attempt.score >= passing_score:
                Certificate.objects.create(user=user, quiz=quiz, score=attempt.score)

            return Response({
                'message': 'Quiz completed',
                'final_score': attempt.score,
                'certificate_generated': attempt.score >= passing_score
            }, status=status.HTTP_200_OK)



class QuizViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)

    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer

class QuestionViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)

    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

# Fetching quiz status (in-progress or completed) and certificates
class QuizStatusView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        user = request.user
        attempts = UserAttempt.objects.filter(user=user).order_by('-id')
        attempts_data = []

        for attempt in attempts:
            data = {
                'quiz': attempt.quiz.title,
                'score': attempt.score,
                'completed': attempt.completed
            }
            if attempt.completed:
                certificate = Certificate.objects.filter(user=user, quiz=attempt.quiz).first()
                if certificate:
                    data['certificate'] = CertificateSerializer(certificate).data

            attempts_data.append(data)

        return Response(attempts_data)

class UserAttemptsView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        user = request.user
        attempts = UserAttempt.objects.filter(user=user).select_related('quiz')
        serializer = UserAttemptSerializer(attempts, many=True)
        return Response(serializer.data)


