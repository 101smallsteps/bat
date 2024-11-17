import React, { useState, useEffect } from 'react';
import { Button, ButtonGroup, Card, Col, Row } from 'react-bootstrap';
import { LinkContainer } from 'react-router-bootstrap';
import { Navigate } from 'react-router-dom';
import "./home.scss";


const Home = (props) => {

 console.log("Home");
  return (
    <div className='middle-center'>
        <>
          {/* Row 1: Full-Width Image Banner */}
          <Row className="my-5">
            <Col>
              <img
                src="/careerFlow.webp?url" // Replace with the actual path to your banner image
                alt="career flow"
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
                    <Card.Title className='text-center'>Certification Exams Available</Card.Title>
                    <Card.Text>
                      <ul style={{  marginLeft: '0', paddingLeft: '0px', lineHeight: '1.8' }}>
                        <li>Personal Finance</li>
                        <li>Basic Business Fundamental Analysis </li>
                      </ul>
                    </Card.Text>
                  </Card.Body>
                </Card>
            </Col>

            <Col md={4}>
                <Card  style={{ backgroundColor: '#c8d7d7', color: 'black', padding: '10px' }}>
                  <Card.Body>
                    <Card.Title className='text-center'>Notice Board</Card.Title>
                    <Card.Text>
                      <ul style={{  marginLeft: '0', paddingLeft: '0px', lineHeight: '1.8' }}>
                        <li>2024-2025 High School Bootcamp Leadership Program</li>
                        <li>click to apply</li>
                      </ul>
                    </Card.Text>
                  </Card.Body>
                </Card>
            </Col>

            <Col md={4}>
                <Card  style={{ backgroundColor: '#c8d7d7', color: 'black', padding: '10px' }}>
                  <Card.Body>
                    <Card.Title className='text-center'>Research and White Papers to Conduct</Card.Title>
                    <Card.Text>
                      <ul style={{  marginLeft: '0', paddingLeft: '0px', lineHeight: '1.8' }}>
                        <li>Work in progress</li>
                          <ul style={{  marginLeft: '10', paddingLeft: '10px', lineHeight: '1.8' }}>
                            <li>The Indicators of Business Failures</li>
                          </ul>
                        <li>Completed</li>
                          <ul style={{  marginLeft: '10', paddingLeft: '10px', lineHeight: '1.8' }}>
                            <li>To be published</li>
                          </ul>
                        <li>Planned</li>
                          <ul style={{  marginLeft: '10', paddingLeft: '10px', lineHeight: '1.8' }}>
                            <li>The Applied Mathematics of Business Failures</li>
                            <li>The Economics of Business Failures</li>
                            <li>Business Failures and Mitigations</li>
                          </ul>
                      </ul>
                    </Card.Text>
                  </Card.Body>
                </Card>
            </Col>
          </Row>
        </>

    </div>
  );
}
export default Home ;
