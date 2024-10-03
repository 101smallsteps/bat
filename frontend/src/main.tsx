import React from 'react'
import ReactDOM from 'react-dom/client'
import ReactDOMClient from 'react-dom/client';
import App from './App.tsx'

const rootElement = document.getElementById('root');

//ReactDOM.createRoot(document.getElementById('root') as HTMLElement).render(
//  <React.StrictMode>
//    <App />
//  </React.StrictMode>,
//)

const root = ReactDOMClient.createRoot(rootElement as HTMLElement); // ✅
root.render(<App />);