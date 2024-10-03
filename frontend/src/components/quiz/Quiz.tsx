import React, { useEffect, useState } from 'react';
import axios from 'axios';
import config from '../../config';
import './Quiz.scss'; // Import the CSS file

type AnswerType = {
    id: number;
    answer_text: string;
};

type QuestionType = {
    id: number;
    question_text: string;
    answers: AnswerType[];
};

type QuizAttemptType = {
    id: number;
    score: number;
    current_question: QuestionType | null;
    completed: boolean;
    total_questions: number;
    current_question_index: number;
};

const getToken = () => {
    const auth_token = window.localStorage.getItem("bat.auth");
    return auth_token ? auth_token.replace(/"/g, "") : '';
};

const Quiz = ({ quizId }: { quizId: number }) => {
    const [attempt, setAttempt] = useState<QuizAttemptType | null>(null);
    const [selectedAnswer, setSelectedAnswer] = useState<number | null>(null);
    const [loading, setLoading] = useState<boolean>(true);
    const [error, setError] = useState<string | null>(null);
    const [certificateMessage, setCertificateMessage] = useState<string | null>(null);
    const [certificateGenerated, setCertificateGenerated] = useState<boolean>(false);

    const backend_server = config.backend_server;
    const api = axios.create({
        baseURL: `${backend_server}/api/`,  // Django backend URL
        headers: {
            'Content-Type': 'application/json',
            "Authorization": `Token ${getToken()}`
        },
    });

    useEffect(() => {
        setLoading(true);
        setError(null);

        // Fetch quiz details and start or resume attempt
        api.post(`cert/quiz/${quizId}/start/`)
            .then((res) => {
                const attemptData: QuizAttemptType = res.data.attempt;  // Accessing the 'attempt' field from the response
                console.log('Quiz Attempt Data:', attemptData);

                if (attemptData.current_question) {
                    setAttempt(attemptData);
                } else {
                    setError('Unexpected response format from server.');
                }
                setLoading(false);
            })
            .catch((err) => {
                console.error('Error starting quiz:', err);
                setError('Failed to start quiz. Please try again.');
                setLoading(false);
            });
    }, [quizId]);

    const handleAnswerSubmit = () => {
        if (selectedAnswer === null || !attempt?.current_question) return;

        // Submit the answer and fetch the next question
        api.post(`cert/quiz/${quizId}/question/${attempt.current_question.id}/submit/`, {
            answer_id: selectedAnswer,
        })
            .then((res) => {
                if (res.data.next_question) {
                    setAttempt(prevAttempt => ({
                        ...prevAttempt!,
                        current_question: res.data.next_question,
                        score: res.data.score,
                        current_question_index: prevAttempt!.current_question_index + 1,
                    }));
                    setSelectedAnswer(null);
                } else {
                    setAttempt(prevAttempt => ({
                        ...prevAttempt!,
                        completed: true,
                        score: res.data.final_score,
                    }));
                }
            })
            .catch((err) => {
                console.error('Error submitting answer:', err);
                setError('Error submitting answer. Please try again.');
            });
    };

    const handleGenerateCertificate = () => {
        setCertificateMessage(null);  // Reset message
        api.post(`cert/quiz/${quizId}/generate_certificate/`)
            .then((res) => {
                setCertificateMessage(res.data.message);
                setCertificateGenerated(true);
                // Optionally, prompt the user to download the certificate
                window.open(`${backend_server}/api/cert/certificates/download/${res.data.file_name}`, '_blank');
            })
            .catch((err) => {
                console.error('Error generating certificate:', err);
                setCertificateMessage('Error generating certificate. Please try again.');
            });
    };

    if (loading) return <div>Loading quiz...</div>;
    if (error) return <div>Error: {error}</div>;

    if (!attempt || !attempt.current_question) return <div>No questions available.</div>;

    const progressText = `Progress: Question ${attempt.current_question_index + 1} of ${attempt.total_questions}`;

    return (
        <div>
            <h1>Quiz</h1>

            {attempt.completed ? (
                <div className="quiz-card">
                    <h2>Quiz Completed!</h2>
                    <p>Final Score: {attempt.score}</p>
                    <p>Total Questions: {attempt.total_questions}</p>
                    {attempt.score >= (0.8 * attempt.total_questions) ? (
                        <div>
                            <h3>Congratulations!</h3>
                            <p>You have answered 80% of the questions correctly.</p>
                            <button onClick={handleGenerateCertificate}>Download Certificate</button>
                        </div>
                    ) : (
                        <div>
                            <h3>Better luck next time!</h3>
                            <p>You need to answer at least 80% of the questions to receive a certificate.</p>
                        </div>
                    )}
                    {certificateMessage && <p>{certificateMessage}</p>}
                </div>
            ) : (
                <div className="quiz-card">
                    <p>{progressText}</p>
                    <div className="question-card">
                        <p>{attempt.current_question.question_text}</p>
                        {attempt.current_question.answers.map((answer) => (
                            <div className="answer-option" key={answer.id}>
                                <input
                                    type="radio"
                                    name="answer"
                                    value={answer.id}
                                    checked={selectedAnswer === answer.id}
                                    onChange={() => setSelectedAnswer(answer.id)}
                                />
                                {answer.answer_text}
                            </div>
                        ))}
                        <button className="submit-button" onClick={handleAnswerSubmit} disabled={selectedAnswer === null}>
                            Submit Answer
                        </button>
                    </div>
                </div>
            )}
        </div>
    );
};

export default Quiz;
