import React, { useEffect, useState } from 'react';
import axios from 'axios';
import config from '../../config';
import './QuizList.scss'; // Import your CSS file for styling

type QuizType = {
    id: number;
    title: string;
    total_questions: number;
};

const getToken = () => {
    const auth_token = window.localStorage.getItem("bat.auth");
    return auth_token ? auth_token.replace(/"/g, "") : '';
};

const QuizList: React.FC = () => {
    const [quizzes, setQuizzes] = useState<QuizType[]>([]);
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

        // Fetch available quizzes
        api.get('cert/quizzes/')
            .then((res) => {
                setQuizzes(res.data.results);
                setLoading(false);
            })
            .catch((err) => {
                console.error('Error fetching quizzes:', err);
                setError('Failed to fetch quizzes. Please try again.');
                setLoading(false);
            });
    }, []);

    if (loading) return <div>Loading quizzes...</div>;
    if (error) return <div>Error: {error}</div>;

    return (
        <div className="quiz-list">
            <h1>Available Quizzes</h1>
            <div className="quiz-cards">
                {quizzes.map((quiz) => (
                    <div key={quiz.id} className="quiz-card">
                        <h2>{quiz.title}</h2>
                        <p>Total Questions: {quiz.total_questions}</p>
                        <button onClick={() => window.location.href = `/quiz/${quiz.id}`}>
                            Start Quiz
                        </button>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default QuizList;
