import React from 'react';
import './GetParkingPass.css';
import { useState } from 'react';
import { ApiClientPost } from './ApiClient.jsx';

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
      response = await ApiClientPost("/parkingPass/", parkingPassForm);
    } catch (error) {
      alert('Failed to add parking pass. Please try again.');
      console.error('Error submitting form:', error);
    } finally {
      setLoading(false);
      if (response.status !== 500) 
      {
        alert('Parking pass purchased successfully!');
        window.location.href = "/passSuccess";
      } 
    }

  };
  
  return (
      <form onSubmit={handleSubmit} className="pass-form">
      <div className="form-header">
        <h1>Get Parking Pass</h1>
        <p>Enter your information below:</p>
      </div>
      <div className="row0">
        <input name="name" placeholder="John Doe" onChange={handleChange} value={parkingPassForm.name} required />
        <input name="licensePlate" placeholder="ABC123" onChange={handleChange} value={parkingPassForm.licensePlate} required />
      </div>
      <button type="submit" disabled={loading}>
        {loading ? 'Purchasing Parking Pass...' : 'Submit Details'}
      </button>
      </form>
    );
}

export default GetParkingPass;