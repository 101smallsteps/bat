import React, { useEffect, useState } from 'react';
import axios from 'axios';
import config from '../../config';
import "./UserCertificates.scss";

type CertificateType = {
    id: number;
    quiz_title: string;
    score: number;
    generated_on: string;
};

const getToken = () => {
    const auth_token = window.localStorage.getItem("bat.auth");
    return auth_token ? auth_token.replace(/"/g, "") : '';
};

const UserCertificates = () => {
    const [certificates, setCertificates] = useState<CertificateType[]>([]);
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
        api.get('cert/certificates/')
            .then((res) => {
                setCertificates(res.data);
                setLoading(false);
            })
            .catch((err) => {
                console.error('Error fetching certificates:', err);
                setError('Failed to load certificates.');
                setLoading(false);
            });
    }, []);

    const handleDownload = (certificateId: number) => {
        // Assuming you have an API endpoint that returns a downloadable PDF or image for the certificate
        api.get(`cert/certificates/${certificateId}/download/`, { responseType: 'blob' })
            .then((response) => {
                const url = window.URL.createObjectURL(new Blob([response.data]));
                const link = document.createElement('a');
                link.href = url;
                link.setAttribute('download', `Certificate_${certificateId}.pdf`); // or .jpg/.png
                document.body.appendChild(link);
                link.click();
            })
            .catch((error) => {
                console.error('Error downloading certificate:', error);
            });
    };

    if (loading) return <div>Loading certificates...</div>;
    if (error) return <div>{error}</div>;

    return (
        <div>
            <h1>My Certificates</h1>
            {certificates.length === 0 ? (
                <p>You haven't obtained any certificates yet.</p>
            ) : (
                <div className="certificate-list">
                    {certificates.map(certificate => (
                        <div key={certificate.id} className="certificate-card">
                            <h2>{certificate.quiz_title}</h2>
                            <p>Score: {certificate.score}</p>
                            <p>Generated on: {new Date(certificate.generated_on).toLocaleDateString()}</p>
                            <button onClick={() => handleDownload(certificate.id)}>Download Certificate</button>
                        </div>
                    ))}
                </div>
            )}
        </div>
    );
};

export default UserCertificates;
