import './NavTop.css';
import react from 'react';
import { useSelector } from 'react-redux';

import Container from 'react-bootstrap/Container';
import Nav from 'react-bootstrap/Nav';
import Navbar from 'react-bootstrap/Navbar';

import logo from '../../assets/img/OPRE@3x.png';

const NavTop = () => {
  const user = useSelector((state) => state.auth.user);
 
  return(
    <div className='nav-top'>
      <Navbar bg="dark" data-bs-theme="dark" fixed="top">
        <Container>
          <Navbar.Brand href="/home">
          <img
            alt="OPRE Logo"
            src={logo}
            width="70"
            height="20"
            className="d-inline-block align-top"
          />{' '}
        </Navbar.Brand>
          <Nav className="me-auto">
            <Nav.Link href="home">Home</Nav.Link>
            <Nav.Link href="#features">Features</Nav.Link>
            <Nav.Link href="#pricing">Pricing</Nav.Link>
          </Nav>
          <Navbar.Toggle />
          <Navbar.Collapse className="justify-content-end">
          <Navbar.Text>
            {user && typeof user === "object" && user.username
              ? `Signed in as: ${user.username}`
              : "Sign in"}
          </Navbar.Text>
          </Navbar.Collapse>
        </Container>
      </Navbar>
    </div>
  )
}

export default NavTop;