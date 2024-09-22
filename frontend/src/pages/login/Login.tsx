import React from 'react';
import { GoogleLogin } from '@react-oauth/google';

const Login = ({ googleLogin, isLoggedIn }) => {
  if (isLoggedIn) {
    return <div>You are already logged in!</div>;
  }

  return (
    <div>
      <h1>Login</h1>
      <GoogleLogin
        onSuccess={googleLogin}
        onError={() => {
          console.error('Login failed');
        }}
      />
    </div>
  );
};

export default Login;
