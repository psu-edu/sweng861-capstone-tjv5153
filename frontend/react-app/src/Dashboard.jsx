import React, {useState, useEffect} from 'react';
import ApiClientFetch from './ApiClient.jsx';
import ApiClientGetUserInfo from './ApiClient.jsx';
import { Link } from 'react-router-dom';
import './Dashboard.css';

function Dashboard() {
  const [loading, setLoading] = useState(true);

  ApiClientFetch('/userinfo', {
    credentials: 'include'
  })
    .then(async (response) => {
      const data = await response.json();
      sessionStorage.setItem("user.name", data.user_info.name);
      sessionStorage.setItem('authStatus', true);
    });


  return (<div className="dashboard">
    <div className="dashboard-header">
        <h1>Welcome to the Commuter Dashboard</h1>
        <p>Use the buttons below to navigate:</p>
    </div>
    <ul className="dashboard-buttons">
        <button onClick={() => window.location.href = "/parkingPass"}>Get Parking Pass</button>
        <button onClick={() => window.location.href = "/checkTickets"}>Check Citations</button>
        <button onClick={() => window.location.href = "/licensePlate"}>Garage Access</button>
    </ul>
  </div>);
}

export default Dashboard;