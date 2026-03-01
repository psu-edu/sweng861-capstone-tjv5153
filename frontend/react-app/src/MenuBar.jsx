import React, {useState, useEffect} from 'react';
import { Link } from 'react-router-dom';
import './MenuBar.css';
import logo from "./assets/logo.ico"; 

const MenuBar = () => {

    const [userName, setUserName] = useState(() => {
        return sessionStorage.getItem('user.name') || 'Guest';
    });
    
    useEffect(() => {
        const updateName = () => setUserName(sessionStorage.getItem('user.name') || 'Guest');

        const handleStorageChange = (e) => {
            if (!e || e.key === 'user.name') updateName();
        };

        window.addEventListener('storage', handleStorageChange);
        const poll = setInterval(updateName, 50);

        return () => {
            window.removeEventListener('storage', handleStorageChange);
            clearInterval(poll);
        };
    }, []);

  return (
    <nav className="menu-bar">
        <div className="menu-logo">
            <a href="/">
            <img src={logo} alt="Tim Volkar" className="logo-img"/>
            </a>
        </div>
        <ul className="menu-links">
            <li><Link to="/">Home</Link></li>
            <li><Link to="/dashboard">Commuter Dashboard</Link></li>
            <li><Link to="/officerDashboard">Officer Dashboard</Link></li>
            <li><Link to="/login">Login</Link></li>
        </ul>
        <div className="nav-user-status">
            {`Hello, ${userName}`}
        </div>
    </nav>
  );
};

export default MenuBar;
