// src/pages/AuthCallback.js
import React, { useEffect } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import axios from 'axios';
import config from '../../config';

const AuthCallback = () => {
  const navigate = useNavigate();
  const location = useLocation();

  useEffect(() => {
    const query = new URLSearchParams(location.search);
    const code = query.get('code');
    const token = query.get('access_token');

    console.log("Authorization Code:", code);

    if (code) {
      // Exchange code for tokens on the backend
      axios.post(`${config.backend_server}/api/auth/google-login/`, {code})
        .then(response => {
          window.localStorage.setItem('bat.auth', JSON.stringify(response.data.key));
          navigate('/home');
        })
        .catch(error => {
          console.error('Error during token exchange', error);
          navigate('/login');
        });
    } else if (token) {
      // Handle implicit flow tokens
      window.localStorage.setItem('bat.auth', token);
      navigate('/home');
    } else {
      navigate('/login');
    }
  }, [location, navigate]);

  return <div>Loading...</div>;
};

export default AuthCallback;
