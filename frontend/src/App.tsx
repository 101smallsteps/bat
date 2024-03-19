import React, { useState } from 'react';
import Home from "./pages/home/Home";
import { createBrowserRouter, RouterProvider, Outlet } from "react-router-dom";
import Users from "./pages/users/Users";
import Products from "./pages/products/Products";
import Portfolio from "./pages/portfolio/Portfolio";
import PortfolioAnalysis from "./pages/portfolioanalysis/PortfolioAnalysis";
import Navbar from "./components/navbar/Navbar";
import Footer from "./components/footer/Footer";
import Menu from "./components/menu/Menu";
import Landing from "./pages/landing/landing";
import Login from "./pages/login/Login";
import Signup from "./pages/signup/Signup";
import "./styles/global.scss";
import 'bootswatch/dist/lumen/bootstrap.css'; // new
import User from "./pages/user/User";
import Product from "./pages/product/Product";
import Analysis from "./pages/analysis/Analysis";
import axios from 'axios';
import {
  QueryClient,
  QueryClientProvider,
} from "@tanstack/react-query";
import { LinkContainer } from 'react-router-bootstrap';
import ReactDOM from "react-dom";
import { Navigate } from 'react-router-dom';

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
    var n_tok=auth_token.replace(/"/g, "");
   return n_tok;
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
            const backend_server = process.env.BACKEND_SERVER;
            const response = await axios.get(
                `${backend_server}/api/auth/user/`,
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

    // changed
    const logIn = async (username, password) => {
      const backend_server = process.env.BACKEND_SERVER;
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

    const logout = async () => {
      const backend_server = process.env.BACKEND_SERVER;
      const url = `${backend_server}/api/auth/logout/`;
      try {
        const response = await axios.post(url);

         window.localStorage.removeItem('bat.auth');
         setLoggedIn(false);
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
          path: "/users/:id",
          element: <User
          profData={userData}
           />,
        }

      ],
    },
    {
      path: "/login",
      element:
      <Login
        isLoggedIn={isLoggedIn}
        logIn={logIn}
      />,
    },
    {
      path: "/signup",
      element: <Signup />,

    }
  ]);

  return  <RouterProvider router={router} />;

}


function Layout (props:Prop)  {
   let menu_item;
   console.log("==props==");
    console.log(props);


   if (props.isLoggedIn){
        menu_item=<Menu />
   }
   else
   {
        menu_item=""
   }

    return (
    <>
      <div className="main">
        <Navbar UserName={props.userData.username} isLoggedIn={props.isLoggedIn} logOutCallback={props.logout}/>
        <div className="container">
          <div className="menuContainer">
            {menu_item}
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
