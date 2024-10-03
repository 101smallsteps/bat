import React, { useEffect, useState } from 'react';
import axios from 'axios';
import config from '../../config';

type UserAttemptType = {
    id: number;
    quiz: {
        title: string;
    };
    score: number;
    completed: boolean;
    completed_at: string | null;
};

const getToken = () => {
    const auth_token = window.localStorage.getItem("bat.auth");
    return auth_token ? auth_token.replace(/"/g, "") : '';
};

const UserAttempts: React.FC = () => {
    const [attempts, setAttempts] = useState<UserAttemptType[]>([]);
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

        // Fetch user attempts
        api.get('cert/certificates/')
            .then((res) => {
                setAttempts(res.data);
                setLoading(false);
            })
            .catch((err) => {
                console.error('Error fetching user attempts:', err);
                setError('Failed to fetch attempts. Please try again.');
                setLoading(false);
            });
    }, []);

    if (loading) return <div>Loading attempts...</div>;
    if (error) return <div>Error: {error}</div>;

    return (
        <div>
            <h1>Your Quiz Attempts</h1>
            <ul>
                {attempts.map((attempt) => (
                    <li key={attempt.id}>
                        <strong>{attempt.quiz.title}</strong> - Score: {attempt.score}
                        {attempt.completed ? (
                            <span>
                                {' '} - Completed
                                <a href={`/certificate/${attempt.id}`}> View Certificate</a>
                            </span>
                        ) : (
                            <span> - In Progress</span>
                        )}
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default UserAttempts;
