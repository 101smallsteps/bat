// config.ts
//const config = {
//    backend_server: 'https://core.bat4all.com' // Set your default API URL here
//};

const baseURL = process.env.NODE_ENV === 'production' ? 'https://bat4all.com' : 'http://localhost:8080';

const config = {
    backend_server: `${baseURL}` ,// Set your default API URL here,
    //google_client_id: process.env.GOOGLE_CLIENT_ID
    google_client_id:''

};


export default config;
