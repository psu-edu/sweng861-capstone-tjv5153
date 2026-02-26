import React from 'react';
import { Link } from 'react-router-dom';
import './MenuBar.css';
import logo from "./assets/logo.ico"; 

const MenuBar = () => {
  return (
    <nav className="menu-bar">
        <div className="menu-logo">
            <a href="/">
            <img src={logo} alt="Tim Volkar" className="logo-img"/>
            </a>
        </div>
        <ul className="menu-links">
            <li><Link to="/">Home</Link></li>
            <li><Link to="/login">Login</Link></li>
        </ul>
        <div className="nav-user-status">
            {sessionStorage.getItem("user.name") ? `Hello, ${sessionStorage.getItem("user.name")}` : 'Hello, Guest'}
        </div>
    </nav>
  );
};

export default MenuBar;
