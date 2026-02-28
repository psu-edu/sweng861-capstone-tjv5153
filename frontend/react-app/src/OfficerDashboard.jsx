import React, {useState, useEffect} from 'react';
import ApiClientFetch from './ApiClient.jsx';
import ApiClientGetUserInfo from './ApiClient.jsx';
import { Link } from 'react-router-dom';
import './OfficerDashboard.css';

function OfficerDashboard() {
  const [loading, setLoading] = useState(true);

  ApiClientFetch('/userinfo', {
    credentials: 'include'
  })
    .then(data => {
        sessionStorage.setItem("user.name", data.user_info.name);
        sessionStorage.setItem('authStatus', true);
    });

    return (<div className="dashboard">
    <div className="dashboard-header">
        <h1>Welcome to the Officer Dashboard</h1>
        <p>Use the buttons below to navigate:</p>
    </div>
    <ul className="dashboard-buttons">
        <button onClick={() => window.location.href = "/citation"}>Write Parking Citation</button>
        <button onClick={() => window.location.href = "/revokePass"}>Revoke Parking Pass</button>
        <button onClick={() => window.location.href = "/removeTicket"}>Remove Parking Citation</button>
    </ul>
  </div>);
}

export default OfficerDashboard;