import { GoogleOAuthProvider,GoogleLogin  } from '@react-oauth/google';
import React, { useState,useEffect } from 'react';
import Home from "./pages/home/Home";
import { createBrowserRouter, RouterProvider, Outlet } from "react-router-dom";
import Users from "./pages/users/Users";
import Products from "./pages/products/Products";
import Portfolio from "./pages/portfolio/Portfolio";
import PortfolioAnalysis from "./pages/portfolioanalysis/PortfolioAnalysis";
import Navbar from "./components/navbar/Navbar";
import Footer from "./components/footer/Footer";
import Menu from "./components/menu/Menu";
import UserAttempts from "./components/userAttempts/UserAttempts";
import UserCertificates from "./components/userCertificates/UserCertificates";
import Landing from "./pages/landing/landing";
import Courses from "./pages/courses/Courses";
import CourseDetail from "./pages/courseDetail/CourseDetail";
import Contributors from "./pages/contributors/Contributors";

import Login from "./pages/login/Login";
import Login_dev from "./pages/login_dev/Login_dev";
import Signup from "./pages/signup/Signup";
import "./styles/global.scss";
import 'bootswatch/dist/lumen/bootstrap.css'; // new
import User from "./pages/user/User";
import Product from "./pages/product/Product";
import Analysis from "./pages/analysis/Analysis";
import AuthCallback from "./pages/authcallback/authcallback";
import QuizListPage from './pages/quizlist/quizlist';
import QuizPage from './pages/quiz/quiz';
import axios from 'axios';
import {
  QueryClient,
  QueryClientProvider,
} from "@tanstack/react-query";
import { LinkContainer } from 'react-router-bootstrap';
import ReactDOM from "react-dom";
import { Navigate } from 'react-router-dom';
import config from './config';

ReactDOM.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
  document.getElementById('root')
);



axios.defaults.xsrfCookieName = 'csrftoken'; // new
axios.defaults.xsrfHeaderName = 'X-CSRFToken'; // new

const getToken = ()=> {
   var auth_token =window.localStorage.getItem("bat.auth");
   return auth_token ? auth_token.replace(/"/g, "") : null;

};


function App() {

    // changed
    const [isLoggedIn, setLoggedIn] = useState(() => {
      return window.localStorage.getItem('bat.auth') !== null;
    });

    const [userData,setuserData] = useState({});

    const getCurrentUser = async () => {
        var tok="Token "+getToken();
        //let tok_str='Token a8a31d16b64a1fa1e02de3401d2a78a1738977cd';
        try {
            const backend_server = config.backend_server;
            const response = await axios.get(
                `https://${backend_server}/api/auth/user/`,
                {
                    'headers':{
                        "Content-Type": "application/json",
                        "Authorization": `${tok}`
                    }
                }
            );
            console.log("UserData");
            console.log(response);
            setuserData({'id':response.data.pk,'username':response.data.username,'email':response.data.email});
            console.log(userData);
            return {response,isError:false};
        }
        catch (error){
            return {error,isError:true};
        }
    }

    // Define the function that detects cross-site tracking prevention
    const detectTrackingPrevention = () => {
        try {
            localStorage.setItem('test', 'testValue');
            localStorage.removeItem('test');
            console.log('Cross-Site Tracking is likely disabled.');
        } catch (e) {
            console.log('Cross-Site Tracking is likely enabled, or storage is blocked.');
            alert('To use Google Sign-In, please disable "Prevent Cross-Site Tracking" in your Safari settings.');
        }
    };

    // Utility to detect if the browser is Safari
    const isSafari = () => {
        return navigator.userAgent.includes('Safari') && !navigator.userAgent.includes('Chrome');
    };
    // changed
    const logIn = async (username, password) => {
      const backend_server = config.backend_server;
      const url = `${backend_server}/api/auth/login/`;
      try {
        const response = await axios.post(url, { username, password });
        console.log(response);
        window.localStorage.setItem(
          'bat.auth', JSON.stringify(response.data.key)
        );
        setLoggedIn(true);
        getCurrentUser();
        console.log(userData);
        return { response, isError: false };
      }
      catch (error) {
        console.error(error);
         return { response: error, isError: true };
      }
    };

    const googleLogin = async (credentialResponse) => {
        const { credential } = credentialResponse;
        // Call the detectTrackingPrevention function inside useEffect
        //console.log('Received Google credential:', credential);
        try {
            const backend_server = config.backend_server;
            const url = `${backend_server}/api/auth/google-login/`; // Your backend endpoint
            const response = await axios.post(url, { token: credential });
            if (isSafari()) {
                    detectTrackingPrevention();
            }

            //console.log('Google login called:')
            if (response.data.redirectUrl) {
               history.push(response.data.redirectUrl);
            } else {
                 window.localStorage.setItem('bat.auth', JSON.stringify(response.data.key));
                  setLoggedIn(true);
                  await getCurrentUser(); // Assuming you have this function defined
            }
        } catch (error) {
            if (error.message.includes('Cross-Site Tracking')) {
                alert('To use Google Sign-In, please disable "Prevent Cross-Site Tracking" or use a different browser ');
            } else {
                console.error('Google login failed:', error);
            }
        }
    }

    const logout = async () => {
      const backend_server = config.backend_server;
      const url = `${backend_server}/api/auth/logout/`;
      try {
        const response = await axios.post(url);

         window.localStorage.removeItem('bat.auth');
         setLoggedIn(false);
         setuserData({});
         console.log("logout done");

      }
      catch (error) {

        console.error(error);
         return { response: error, isError: true };
      }

    };



  const router = createBrowserRouter([
    {
      path: "/",
      element: <Layout isLoggedIn={isLoggedIn} logout={logout} userData={userData}/>,
      children: [
        {
          path: "/",
          index: true,
          element: <Landing
          isLoggedIn={isLoggedIn}
          />,
        },
        {
          path: "/home",
          element: <Home
          isLoggedIn={isLoggedIn}
          />,
        },
        {
          path: "/portfolio",
          element: <Portfolio />,
        },
        {
          path: "/portfolio/:id",
          element: <Portfolio />,
        },
        {
          path: "/portfolioAnalysis",
          element: <PortfolioAnalysis />,
        },
        {
          path: "/portfolioAnalysis/:id",
          element: <Analysis />,
        },
        {
          path: "/courses",
          element: <Courses />,
        },
        {
          path: "/courses/:courseId",
          element: <CourseDetail />,
        },
        {
            path: "/quizlist",
            element: <QuizListPage />,
        },
        {
            path: "/quiz/:quizId",
            element: <QuizPage />,
        },
        {
          path: "/certificates",
          element: <UserCertificates />,
        },
        {
          path: "/history",
          element: <UserAttempts />,
        },
        {
          path: "/users/:id",
          element: <User
          profData={userData}
           />,
        },
      // Add the callback route
      {
        path: "/auth/callback",
        element: <AuthCallback />,
      },
      ],
    },
...(process.env.NODE_ENV === 'production'
    ? [
        {
          path: "/login",
          element: <Login googleLogin={googleLogin} isLoggedIn={isLoggedIn} />,
        },
      ]
    : []),
...(process.env.NODE_ENV === 'development'
    ? [
        {
          path: "/login",
          element: <Login_dev logIn={logIn} isLoggedIn={isLoggedIn} />,
        },
      ]
    : []),
    {
      path: "/signup",
      element: <Signup />,

    }
  ]);

        if (process.env.NODE_ENV === 'development') {
            return  <RouterProvider router={router} />;
        }
        else {
          return (
            <GoogleOAuthProvider clientId={config.google_client_id}>  {/* Client ID passed from config */}
              <RouterProvider router={router} />
              {!isLoggedIn && (
                <GoogleLogin
                  type="standard"
                   theme="outline"
                    size="large"
                    text="signin_with"
                    shape="rectangular"
                    clientId={config.google_client_id}
                     uxMode="redirect"
                    redirectUri={config.backend_auth_callback}
                    onSuccess={googleLogin}
                  onError={(error) => console.error("Google Login Error:", error)}
                />
              )}
            </GoogleOAuthProvider>
          );
        }

 }

function Layout(props) {
  const { isLoggedIn, userData, logout } = props;

  return (
    <>
      <div className="main">
        <Navbar UserName={userData.username} isLoggedIn={isLoggedIn} logOutCallback={logout} />
        <div className="container">
          <div className="menuContainer">
            {isLoggedIn && <Menu />}
          </div>
          <div className="contentContainer">
            <Outlet />
          </div>
        </div>
        <Footer />
      </div>
    </>
  );
}


export default App;
