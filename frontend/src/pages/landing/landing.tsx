// client/src/components/Landing.js

import React, { useState, useEffect } from 'react';
import { Button, ButtonGroup } from 'react-bootstrap'; // new
import { LinkContainer } from 'react-router-bootstrap'; // new
import { useNavigate  } from 'react-router-dom';
import { Navigate } from 'react-router-dom';

const Landing = (props) => {
  const [redirect, setRedirect] = useState(false);

  useEffect(() => {
    const timer = setTimeout(() => {
      setRedirect(true);
    }, 10); // Redirect after 5 seconds (adjust as needed)

    return () => clearTimeout(timer); // Cleanup the timer on component unmount
  }, []);

  return (
    <div className='middle-center'>
      <h1 className='landing logo'>Re-defining business analysis </h1>
        {
        props.isLoggedIn ? (
          <Navigate to='/home' />
        ) : (
        <>
        { process.env.NODE_ENV === 'development' && (
              // Enable the below block of code if google sign has problems and you need to triage
              <ButtonGroup>
                <LinkContainer to='/signup'>
                  <Button data-cy="signUp">Sign up</Button>
                </LinkContainer>
                <LinkContainer to='/login'>
                  <Button data-cy="logIn">Log in</Button>
                </LinkContainer>
               </ButtonGroup>
          )}
            <h1 className='landing logo'></h1>
          </>

            )
      }
    </div>
  );
}

export default Landing