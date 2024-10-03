import React, { useEffect, useState } from 'react';
import axios from 'axios';
import config from '../../config';
import './Quiz.scss'; // Import your CSS file for styling

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

const Quiz: React.FC<{ quizId: number }> = ({ quizId }) => {
    const [attempt, setAttempt] = useState<QuizAttemptType | null>(null);
    const [selectedAnswer, setSelectedAnswer] = useState<number | null>(null);
    const [loading, setLoading] = useState<boolean>(true);
    const [error, setError] = useState<string | null>(null);

    const backend_server = config.backend_server;
    const api = axios.create({
        baseURL: `${backend_server}/api/`,
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
                const attemptData: QuizAttemptType = res.data.attempt;
                setAttempt(attemptData);
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

    if (loading) return <div>Loading quiz...</div>;
    if (error) return <div>Error: {error}</div>;

    if (!attempt || !attempt.current_question) return <div>No questions available.</div>;

    return (
        <div className="quiz-container">
            <h1>Quiz: {attempt.quiz.title}</h1>
            <div className="quiz-card">
                <p>Progress: Question {attempt.current_question_index + 1} of {attempt.total_questions}</p>
                <h2>{attempt.current_question.question_text}</h2>
                {attempt.current_question.answers.map((answer) => (
                    <div key={answer.id}>
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
                <button onClick={handleAnswerSubmit} disabled={selectedAnswer === null}>
                    Submit Answer
                </button>
            </div>
        </div>
    );
};

export default Quiz;
