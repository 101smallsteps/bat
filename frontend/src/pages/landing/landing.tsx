import React, { useState, useEffect } from 'react';
import { Button, ButtonGroup, Card, Col, Row } from 'react-bootstrap';
import { LinkContainer } from 'react-router-bootstrap';
import { Navigate } from 'react-router-dom';

const Landing = (props) => {
  const [redirect, setRedirect] = useState(false);

  useEffect(() => {
    const timer = setTimeout(() => {
      setRedirect(true);
    }, 10000); // Redirect after 10 seconds

    return () => clearTimeout(timer);
  }, []);

  return (
    <div className='middle-center'>

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

          {/* Row 1: Full-Width Image Banner */}
          <Row className="my-5">
            <Col>
              <img
                src="/financial_literacy.webp?url" // Replace with the actual path to your banner image
                alt="Financial Literacy Banner"
                className="img-fluid w-100"
                style={{
                  borderRadius: '8px',
                  maxHeight: '220px', // Adjust for desired banner height
                  objectFit: 'cover',
                }}
              />
            </Col>
          </Row>

          {/* Row 2: First set of responsive cards */}
          <Row className='mb-4'>
            <Col md={4}>
                <Card  style={{ backgroundColor: '#c8d7d7', color: 'black', padding: '10px' }}>
                  <Card.Body>
                    <Card.Title className='text-center'>Our Mission</Card.Title>
                    <Card.Text>
                      <ul style={{  marginLeft: '0', paddingLeft: '0px', lineHeight: '1.8' }}>
                        <li>Open source</li>
                        <li>Provide AI-based financial recommendations and advice</li>
                        <li>Conduct research on business failures and spread findings</li>
                        <li>Build analytical tools that can save small businesses</li>
                      </ul>
                    </Card.Text>
                  </Card.Body>
                </Card>
            </Col>

            <Col md={4}>
                <Card  style={{ backgroundColor: '#c8d7d7', color: 'black', padding: '10px' }}>
                  <Card.Body>
                    <Card.Title className='text-center'>Our Vision</Card.Title>
                    <Card.Text>
                      <ul style={{  marginLeft: '0', paddingLeft: '0px', lineHeight: '1.8' }}>
                        <li>Empower individuals, small investors, and small businesses with analytical knowledge and tools</li>
                        <li>Improve financial literacy among the student community</li>
                        <li>Strive towards zero-tolerance of small businesses failing across the world</li>
                      </ul>
                    </Card.Text>
                  </Card.Body>
                </Card>
            </Col>

            <Col md={4}>
                <Card  style={{ backgroundColor: '#c8d7d7', color: 'black', padding: '10px' }}>
                  <Card.Body>
                    <Card.Title className='text-center'>Research & Development</Card.Title>
                    <Card.Text>
                      <ul style={{  marginLeft: '0', paddingLeft: '0px', lineHeight: '1.8' }}>
                        <li>Current Research planned</li>
                          <ul style={{  marginLeft: '10', paddingLeft: '10px', lineHeight: '1.8' }}>
                            <li>The Indicators of Business Failures</li>
                            <li>The Applied Mathematics of Business Failures</li>
                            <li>The Economics of Business Failures</li>
                            <li>Business Failures and Mitigations</li>
                            <li>click to apply</li>
                          </ul>
                      </ul>
                    </Card.Text>
                  </Card.Body>
                </Card>
            </Col>
          </Row>
          {/* Row 4: Full-width notice board card */}
          <Row className='mb-5'>
            <Col>
                <Card  style={{ backgroundColor: '#c8d7d7', color: 'black', padding: '10px' }}>
                  <Card.Body>
                    <Card.Title className='text-center'>High School Program</Card.Title>
                    <Card.Text>
                      <ul style={{  marginLeft: '0', paddingLeft: '0px', lineHeight: '1.8' }}>
                        <li>Leadership Program  </li>
                          <ul style={{  marginLeft: '10', paddingLeft: '10px', lineHeight: '1.8' }}>
                            <li>Get trained on business metrics and fundamental analysis</li>
                            <li>Prove your leadership skill by conducting a one day bootcamp event in your school</li>
                            <li>Get certified for your leadership skill from www.101smallsteps.com</li>
                            <li>click to apply</li>
                          </ul>
                      </ul>
                    </Card.Text>
                  </Card.Body>
                </Card>
            </Col>
          </Row>
        </>
      )}
    </div>
  );
}

export default Landing;
