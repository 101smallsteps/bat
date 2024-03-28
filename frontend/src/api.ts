import axios, { AxiosResponse } from 'axios';

const baseURL = process.env.NODE_ENV === 'production' ? 'https://bat4all' : 'http://localhost:8080';

const instance = axios.create({
  baseURL: `${baseURL}/api`,  // Set the base URL for Axios requests
});