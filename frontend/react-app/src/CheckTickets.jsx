import React from 'react';
import './CheckTickets.css';
import { useState } from 'react';
import ApiClientFetch, { ApiClientPost } from './ApiClient.jsx';

function CheckTickets() {
    const [tixCheck, setTixCheck] = useState({
    licensePlate: ''
  });
  const [tickets, setTickets] = useState([]);

  let response = null;
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setTixCheck(prev => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    if (tixCheck.licensePlate.length < 1) {
        alert('License plate cannot be empty.');
        setLoading(false);
        return;
    }

    try {
      response = await ApiClientFetch(`/checkTickets/${tixCheck.licensePlate}`, tixCheck);
    } catch (error) {
      alert('Failed to check tickets. Please try again.');
      console.error('Error submitting form:', error);
    } 
    finally {
        setLoading(false);
        if (response && response.status === 200) {
            const data = await response.json();
            setTickets(data);    
        }
        else {
            alert("Failed To Check Tickets. Try Again.")
        }
    }
  };
  
  return (
      <form onSubmit={handleSubmit} className="checkTix-form">
      <div className="form-header">
        <h1>Check Citations</h1>
        <p>Enter License Plate to Check Citations:</p>
      </div>
        <div className="row0">
        <input name="licensePlate" placeholder="License Plate" onChange={handleChange} value={tixCheck.licensePlate} required />
      </div>
      <button type="submit" disabled={loading}>
        {loading ? 'Checking Tickets...' : 'Submit Details'}
      </button>
      <div className="tickets-list">
        {tickets.length > 0 ? (
          tickets.map((ticket, index) => (
            <div key={index} className="ticket-item">
                <p><strong>Officer Name:</strong> {ticket.officerName}</p>
                <p><strong>Ticket Number:</strong> {ticket.ticketNumber}</p>
                <p><strong>Issue Date:</strong> {ticket.issueDate}</p>
                <p><strong>Fine Amount:</strong> ${ticket.fineAmount}</p>
                <p><strong>Violation:</strong> {ticket.violation}</p>
            </div>
          ))) : (
          <p></p>
        )}
      </div>
      </form>
    );
}

export default CheckTickets;