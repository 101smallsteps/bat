import React, { useEffect, useState } from 'react';
import axios from 'axios';
import config from '../../config';
import "./History.scss";

type UserAttemptType = {
    id: number;
    quiz_title: string;
    score: number;
    completed_at: string | null;
    certification_granted: boolean;
};

const getToken = () => {
    const auth_token = window.localStorage.getItem("bat.auth");
    return auth_token ? auth_token.replace(/"/g, "") : '';
};

const History = () => {
    const [grantedAttempts, setGrantedAttempts] = useState<UserAttemptType[]>([]);
    const [notGrantedAttempts, setNotGrantedAttempts] = useState<UserAttemptType[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);
    const [message, setMessage] = useState<string | null>(null);  // To handle empty responses
    const [activeTab, setActiveTab] = useState<'granted' | 'notGranted'>('granted');

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
        api.get('cert/attempts/')
            .then((res) => {
                if (res.data.message) {
                    setMessage(res.data.message);  // Set message if no attempts
                } else {
                    setGrantedAttempts(res.data.certification_granted);
                    setNotGrantedAttempts(res.data.certification_not_granted);
                }
                setLoading(false);
            })
            .catch((err) => {
                console.error('Error fetching user attempts:', err);
                setError('Failed to load attempts. Please try again.');
                setLoading(false);
            });
    }, []);

    if (loading) return <div>Loading...</div>;
    if (error) return <div>Error: {error}</div>;

    return (
        <div>
            <h1>Your Quiz Attempts</h1>

            {message ? ( // If message exists, display it
                <p>{message}</p>
            ) : (
                <>
                    {/* Tab Navigation */}
                    <div className="tabs">
                        <button className={activeTab === 'granted' ? 'active' : ''} onClick={() => setActiveTab('granted')}>
                            Certificates Granted
                        </button>
                        <button className={activeTab === 'notGranted' ? 'active' : ''} onClick={() => setActiveTab('notGranted')}>
                            Certificates Not Granted
                        </button>
                    </div>

                    {/* Tab Content */}
                    <div className="tab-content">
                        {activeTab === 'granted' && (
                            <div className="attempts-list">
                                {grantedAttempts.length > 0 ? (
                                    grantedAttempts.map((attempt) => (
                                        <div key={attempt.id} className="attempt-card">
                                            <h3>{attempt.quiz_title}</h3>
                                            <p>Score: {attempt.score}</p>
                                            <p>Completed at: {attempt.completed_at}</p>
                                            <button>Download Certificate</button>
                                        </div>
                                    ))
                                ) : (
                                    <p>No certificates granted yet.</p>
                                )}
                            </div>
                        )}

                        {activeTab === 'notGranted' && (
                            <div className="attempts-list">
                                {notGrantedAttempts.length > 0 ? (
                                    notGrantedAttempts.map((attempt) => (
                                        <div key={attempt.id} className="attempt-card">
                                            <h3>{attempt.quiz_title}</h3>
                                            <p>Score: {attempt.score}</p>
                                            <p>Completed at: {attempt.completed_at}</p>
                                            <p>Certification not granted.</p>
                                        </div>
                                    ))
                                ) : (
                                    <p>No attempts without certification.</p>
                                )}
                            </div>
                        )}
                    </div>
                </>
            )}
        </div>
    );
 };

export default History;
