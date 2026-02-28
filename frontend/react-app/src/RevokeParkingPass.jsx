import React from 'react';
import './RevokeParkingPass.css';
import { useState } from 'react';
import { ApiClientPut } from './ApiClient.jsx';

function GetParkingPass() {
    const [parkingPassForm, setparkingPassForm] = useState({
    name: '', licensePlate: ''});
  const [loading, setLoading] = useState(false);
  let response = null;
  
  const handleChange = (e) => {
    const { name, value } = e.target;
    setparkingPassForm(prev => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      response = await ApiClientPut(`/revokeParkingPass/${parkingPassForm.licensePlate}/`);
    } catch (error) {
      if (error && error.message.includes("Bad Request")) {
        alert(`License plate ${parkingPassForm.licensePlate} does not have a parking pass.`);
        setparkingPassForm(prev => ({ ...prev, licensePlate: '' , name: ''}));
      } else {
        alert('Failed to revoke parking pass. Please try again.');
        console.error('Error submitting form:', error.message);
      }
    } finally {
      setLoading(false);
      if (response && response.status == 200) 
      {
        alert('Parking pass revoked successfully!');
        window.location.href = "/officerDashboard";
      } 
    }

  };
  
  return (
      <form onSubmit={handleSubmit} className="pass-form">
      <div className="form-header">
        <h1>Revoke Parking Pass</h1>
        <p>Enter information below:</p>
      </div>
      <div className="row0-pass-form">
        <input name="name" placeholder="John Doe" onChange={handleChange} value={parkingPassForm.name} required />
        <input name="licensePlate" placeholder="ABC123" onChange={handleChange} value={parkingPassForm.licensePlate} required />
      </div>
      <button type="submit" disabled={loading}>
        {loading ? 'Revoking Parking Pass...' : 'Revoke Commuter Pass'}
      </button>
      </form>
    );
}

export default GetParkingPass;