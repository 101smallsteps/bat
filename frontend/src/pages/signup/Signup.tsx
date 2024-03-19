// client/components/SignUp.js

import React, { useState } from 'react';
import { Formik } from 'formik'; // new
import {
  Breadcrumb, Button, Card, Form
} from 'react-bootstrap'; // changed
import { Link, Navigate } from 'react-router-dom';
import axios from 'axios';

const Signup = (props) => {
  const [isSubmitted, setSubmitted] = useState(false);

  const onSubmit = async (values, actions) => {
      const backend_server = process.env.BACKEND_SERVER;
      const url =`${backend_server}/api/auth/register/`;
      const formData = new FormData();
      formData.append('username', values.username);
      formData.append('first_name', values.firstName);
      formData.append('last_name', values.lastName);
      formData.append('email', values.email);
      formData.append('password1', values.password);
      formData.append('password2', values.password);
      formData.append('group', values.group);
      formData.append('photo', values.photo);
      try {
        await axios.post(url, formData);
        setSubmitted(true);
      } catch (response) {
        const data = response.response.data;
        for (const value in data) {
          actions.setFieldError(value, data[value].join(' '));
        }
      }
  };
  if (props.isLoggedIn || isSubmitted) {
    return <Navigate to='/login' />;
  }
  return (
    <>
      <Breadcrumb>
        <Breadcrumb.Item href='/#/'>Home</Breadcrumb.Item>
        <Breadcrumb.Item active>Sign up</Breadcrumb.Item>
      </Breadcrumb>
      <Card className='mb-3'>
        <Card.Header>Sign up</Card.Header>
        <Card.Body>
          <Formik
            initialValues={{
              username: '',
              firstName: '',
              lastName: '',
              password: '',
              email: '',
              group: 'default',
            }}
            onSubmit={onSubmit}
          >
            {({
              errors,
              handleChange,
              handleSubmit,
              isSubmitting,
              setFieldValue,
              values
            }) => (
              <Form noValidate onSubmit={handleSubmit}>
                <Form.Group className='mb-3' controlId='username'>
                  <Form.Label>Username:</Form.Label>
                  <Form.Control
                    className={'username' in errors ? 'is-invalid' : ''}
                    name='username'
                    onChange={handleChange}
                    values={values.username}
                  />
                  {
                    'username' in errors && (
                      <Form.Control.Feedback type='invalid'>{errors.username}</Form.Control.Feedback>
                    )
                  }
                 </Form.Group>
                <Form.Group className='mb-3' controlId='email'>
                  <Form.Label>Email:</Form.Label>
                  <Form.Control
                    className={'email' in errors ? 'is-invalid' : ''}
                    name='email'
                    onChange={handleChange}
                    values={values.email}
                  />
                  {
                    'email' in errors && (
                      <Form.Control.Feedback type='invalid'>{errors.email}</Form.Control.Feedback>
                    )
                  }
                  </Form.Group>
                    <Form.Group className='mb-3' controlId='firstName'>
                      <Form.Label>First name:</Form.Label>
                      <Form.Control
                        className={'firstName' in errors ? 'is-invalid' : ''}
                        name='firstName'
                        onChange={handleChange}
                        required
                        values={values.firstName}
                      />
                      {
                        'firstName' in errors && (
                          <Form.Control.Feedback type='invalid'>{errors.firstName}</Form.Control.Feedback>
                        )
                      }
                    </Form.Group>
                    <Form.Group className='mb-3' controlId='lastName'>
                      <Form.Label>Last name:</Form.Label>
                      <Form.Control
                        className={'lastName' in errors ? 'is-invalid' : ''}
                        name='lastName'
                        onChange={handleChange}
                        required
                        values={values.lastName}
                      />
                      {
                        'lastName' in errors && (
                          <Form.Control.Feedback type='invalid'>{errors.lastName}</Form.Control.Feedback>
                        )
                      }
                    </Form.Group>
                    <Form.Group className='mb-3' controlId='password'>
                      <Form.Label>Password:</Form.Label>
                      <Form.Control
                        className={'password1' in errors ? 'is-invalid' : ''}
                        name='password'
                        onChange={handleChange}
                        required
                        type='password'
                        value={values.password}
                      />
                      {
                        'password1' in errors && (
                          <Form.Control.Feedback type='invalid'>{errors.password1}</Form.Control.Feedback>
                        )
                      }
                    </Form.Group>
                    <Form.Group className='mb-3' controlId='group'>
                      <Form.Label>Group:</Form.Label>
                      <Form.Select
                        className={'group' in errors ? 'is-invalid' : ''}
                        name='group'
                        onChange={handleChange}
                        required
                        value={values.group}
                      >
                        <option value='rider'>Rider</option>
                        <option value='driver'>Driver</option>
                      </Form.Select>
                      {
                        'group' in errors && (
                          <Form.Control.Feedback type='invalid'>{errors.group}</Form.Control.Feedback>
                        )
                      }
                    </Form.Group>
                <div className='d-grid mb-3'>
                  <Button disabled={isSubmitting} type='submit' variant='primary'>Sign up</Button>
                </div>
              </Form>
            )}
          </Formik>
          <Card.Text className='text-center'>
            Already have an account? <Link to='/login'>Log in!</Link>
          </Card.Text>
        </Card.Body>
      </Card>
    </>
  );
}

export default Signup;