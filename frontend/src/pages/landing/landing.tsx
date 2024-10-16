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
                        <li>Empower individuals, small investors, small businesses with knowledge and tools</li>
                        <li>AI-based financial recommendations for everyone</li>
                        <li>Prevent small business failures</li>
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
                        <li>Improve financial literacy among students community</li>
                        <li>Perform research on business failures and share to all</li>
                        <li>Build tools that save business </li>
                        <li>AI-based financial advice for small business</li>
                      </ul>
                    </Card.Text>
                  </Card.Body>
                </Card>
            </Col>

            <Col md={4}>
                <Card  style={{ backgroundColor: '#c8d7d7', color: 'black', padding: '10px' }}>
                  <Card.Body>
                    <Card.Title className='text-center'>Research and development</Card.Title>
                    <Card.Text>
                      <ul style={{  marginLeft: '0', paddingLeft: '0px', lineHeight: '1.8' }}>
                        <li>Current Research planned</li>
                          <ul style={{  marginLeft: '10', paddingLeft: '10px', lineHeight: '1.8' }}>
                            <li>Business failures and indicators</li>
                            <li>Business failures and applied mathematics</li>
                            <li>Business failures and economics</li>
                            <li>Business failures and mitigations</li>
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
                    <Card.Title className='text-center'>High school program</Card.Title>
                    <Card.Text>
                      <ul style={{  marginLeft: '0', paddingLeft: '0px', lineHeight: '1.8' }}>
                        <li>Leadership program  </li>
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
