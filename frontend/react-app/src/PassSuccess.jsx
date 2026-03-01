import React from 'react';
import './PassSuccess.css';

function PassSuccess() {
    return (    
    <div className="success-container">
    <div className="success-header">
        <h1>Parking Pass Added Successfully!</h1>
    </div>
    <div className="success-message">
        <p>Balance of $100 has been added to your LionPath account. Your parking pass has been activated. You can now use it to park in designated areas.</p>
    </div>
    <div className="dashboard-button">
        <button onClick={() => window.location.href = "/dashboard"}>Go to Dashboard</button>
    </div>
  </div>);
}

export default PassSuccess;