import React from 'react';
import './Citation.css';
import { useState } from 'react';
import { ApiClientPost } from './ApiClient.jsx';

function Citation() {
    const [Citation, setCitation] = useState({
    ticketNumber: '', licensePlate: '', issueDate: '', violation: '', fineAmount: 0.0, officerName: ''
  });

  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setCitation(prev => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    if (Citation.fineAmount < 0) {
        alert('Fine amount cannot be negative. Please enter a valid fine amount.');
        setLoading(false);
        return;
    }
    if (Citation.licensePlate.length < 1) {
        alert('License plate cannot be empty.');
        setLoading(false);
        return;
    }
    if (Citation.violation.length < 1) {
        alert('Violation description cannot be empty.');
        setLoading(false);
        return;
    }
    if (Citation.officerName.length < 1) {
        alert('Officer name cannot be empty.');
        setLoading(false);
        return;
    }
    if(Citation.issueDate.length < 1) {
        alert('Issue date cannot be empty.');
        setLoading(false);
        return;
    }
    if(Citation.ticketNumber.length < 1) {
        alert('Ticket number cannot be empty.');
        setLoading(false);
        return;
    }


    try {
      await ApiClientPost("/addTicket", Citation);
    } catch (error) {
      alert('Failed to add citation. Please try again.');
      console.error('Error submitting form:', error);
    } finally {
      setLoading(false);
      alert('Citation added successfully!');
      window.location.href = "/officerDashboard";
    }
  };
  
  return (
      <form onSubmit={handleSubmit} className="citation-form">
      <div className="form-header">
        <h1>Write Citation</h1>
        <p>Complete Each Field Below:</p>
      </div>
      <div className="row0">
        <input name="ticketNumber" placeholder="Ticket Number" onChange={handleChange} value={Citation.ticketNumber} required />
        <input name="licensePlate" placeholder="License Plate" onChange={handleChange} value={Citation.licensePlate} required />
      </div>
      <div className="row1">
        <input name="make" placeholder="Issue Date" onChange={handleChange} value={Citation.issueDate} required />
        <input name="model" placeholder="Fine Amount" onChange={handleChange} value={Citation.fineAmount} required />
      </div>
      <div className="row2">
        <input name="officerName" placeholder="Officer Name" onChange={handleChange} value={Citation.officerName} required />
      </div>
      <div className="row3">
            <input name="violation" type="text" placeholder="Violation Description" onChange={handleChange} value={Citation.violation} required />
        </div>
      <button type="submit" disabled={loading}>
        {loading ? 'Assigning Citation...' : 'Submit Details'}
      </button>
      </form>
    );
}

export default Citation;