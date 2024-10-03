import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import config from '../../config';
import axios from "axios";

type QuizType = {
    id: number;
    title: string;
    total_questions: number;
};

const getToken = ()=> {
   var auth_token =window.localStorage.getItem("bat.auth");
    var n_tok=auth_token.replace(/"/g, "");
   return n_tok;
};

const QuizList = () => {
    const [quizzes, setQuizzes] = useState<QuizType[]>([]);
    const [loading, setLoading] = useState<boolean>(true);
    const [error, setError] = useState<string | null>(null);

    var tok="Token "+getToken();

    const backend_server = config.backend_server;
    const api = axios.create({
        baseURL: `${backend_server}/api/`,  // Django backend URL
        headers: {
            'Content-Type': 'application/json',
            "Authorization": `${tok}`

        },
        });


    useEffect(() => {
        api.get('cert/quizzes/')
            .then((res) => {
                console.log('API Response:', res.data);  // Log the API response to inspect
                if (Array.isArray(res.data.results)) {   // Access the `results` array in the response
                    setQuizzes(res.data.results);        // Set quizzes from the `results` key
                } else {
                    setError('Unexpected response format');
                }
                setLoading(false);
            })
            .catch((err) => {
                console.error('Error fetching quizzes:', err);
                setError('Failed to fetch quizzes');
                setLoading(false);
            });
    }, []);

    if (loading) {
        return <p>Loading quizzes...</p>;
    }

    if (error) {
        return <p>{error}</p>;
    }
    if (quizzes.length === 0) {
        return <p>No quizzes available at the moment.</p>;
    }

    return (
        <div>
            <h1>Available Certifications</h1>
            <ul>
                {quizzes.map((quiz) => (
                    <li key={quiz.id}>
                        {/* Navigate to the quiz detail page */}
                        <Link to={`/quiz/${quiz.id}`}>{quiz.title} (Questions: {quiz.total_questions})</Link>
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default QuizList;
