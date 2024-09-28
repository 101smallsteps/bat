// client/src/components/Landing.tsx

import React, { useState, useEffect } from 'react';
import { Button, ButtonGroup, Card, Col, Row } from 'react-bootstrap'; // Added Card, Col, Row
import { LinkContainer } from 'react-router-bootstrap';
import { Navigate } from 'react-router-dom';

const Landing = (props) => {
  const [redirect, setRedirect] = useState(false);

  useEffect(() => {
    const timer = setTimeout(() => {
      setRedirect(true);
    }, 10000); // Redirect after 10 seconds

    return () => clearTimeout(timer); // Cleanup the timer on component unmount
  }, []);

  return (
    <div className='middle-center'>
      <h1 className='landing logo'>Re-defining Business Analysis (open source)</h1>

      {props.isLoggedIn ? (
        <Navigate to='/home' />
      ) : (
        <>
          {process.env.NODE_ENV === 'development' && (
            <ButtonGroup>
              <LinkContainer to='/signup'>
                <Button data-cy="signUp">Sign up</Button>
              </LinkContainer>
              <LinkContainer to='/login'>
                <Button data-cy="logIn">Log in</Button>
              </LinkContainer>
            </ButtonGroup>
          )}
    <Row className='mt-5'>
      <Col md={4}>
        <Card className='text-center' style={{ backgroundColor: '#f0f0f0' }}>
          <Card.Body>
            <Card.Title>What is Our Goal</Card.Title>
            <Card.Text>
              Our goal is to empower small investors and small businesses around the world with data-driven insights using open-source based tools driven by machine learning that helps to safeguard the capital and the business.
            </Card.Text>
          </Card.Body>
        </Card>
      </Col>

      <Col md={4}>
        <Card className='text-center' style={{ backgroundColor: '#f0f0f0' }}>
          <Card.Body>
            <Card.Title>What We Do</Card.Title>
            <Card.Text>
              We are sponsored by a non-profit company www.101smallsteps.com, we are planning to build financial tools by the students and for the students.
              We provide opportunities to volunteer, contribute and research  for high school, undergraduates, graduates.
            </Card.Text>
          </Card.Body>
        </Card>
      </Col>

      <Col md={4}>
        <Card className='text-center' style={{ backgroundColor: '#f0f0f0' }}>
          <Card.Body>
            <Card.Title>How to Contribute</Card.Title>
            <Card.Text>
              <li>Join our program to create financial clubs in high school.</li>
              <li>Contribute as a developer to create the best tools, machine learning and distributed computing.</li>
              <li>Contribute in our research towards applied mathematics(finance), machine learning , economics.</li>
              <li>Join us in our mission to educate and uplift communities..</li>
            </Card.Text>
          </Card.Body>
        </Card>
      </Col>
    </Row>

          <div className='notice-board mt-5'>
            <h2>Recent Happenings</h2>
            <ul>
              <li>New features launched in tracking fundamentals of stock symbols </li>
              <li>Join our high school club program</li>
              <li>Research activities in machine learning and financial fraud detection </li>
            </ul>
          </div>
        </>
      )}
    </div>
  );
}

export default Landing;
