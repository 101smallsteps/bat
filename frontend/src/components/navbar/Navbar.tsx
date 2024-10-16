import "./navbar.scss";
import { Navigate } from 'react-router-dom';

import {
  Button, Container, Form
} from 'react-bootstrap';

const Navbar = (props:Props) => {
  let logout_btn="";
  if (props.isLoggedIn)
  {
    logout_btn=<Form>
                          <Button
                    data-cy='logOut'
                    type='button'
                    onClick={() => props.logOutCallback()}
      >Log out</Button>
                </Form>
      return (
        <div className="navbar">
          <div className="logo">
            <img src="logo.svg" alt="" />
            <span>BAT - Business AnalyTics</span>
          </div>

          <div className="icons">
          <span>{props.UserName}</span>

          <div>
            {logout_btn}
            </div>
            <div className="user">

            </div>
          </div>
        </div>
      );
  }
  else
  {
    console.log('At home but logged out');
      return (
        <div className='middle-center'>
          <h1 className='landing logo'>BAT - Business AnalyTics for everyone</h1>
            {
            (
              <Navigate to='/' />
            )
          }
        </div>
      );

  }

};

export default Navbar;
