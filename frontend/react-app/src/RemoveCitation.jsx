import React from 'react';
import './RemoveCitation.css';
import { useState } from 'react';
import { ApiClientDelete, ApiClientPut } from './ApiClient.jsx';
import Loading from './Loading.jsx';

function RemoveCitation() {
    const [removeTicketForm, setRemoveTicketForm] = useState({
    ticketNumber: ''});
  const [loading, setLoading] = useState(false);
  let response = null;
  
  const handleChange = (e) => {
    const { name, value } = e.target;
    setRemoveTicketForm(prev => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      setLoading(true);
      response = await ApiClientDelete(`/removeTicket/${removeTicketForm.ticketNumber}/`);
    } catch (error) {
      if (error && error.message.includes("Bad Request")) {
        alert(`Ticket number ${removeTicketForm.ticketNumber} does not exist.`);
        setRemoveTicketForm(prev => ({ ...prev, ticketNumber: '' }));
      } else {
        alert('Failed to remove citation. Please try again.');
        console.error('Error submitting form:', error.message);
      }
    } finally {
      setLoading(false);
      if (response && response.status == 200) 
      {
        alert('Citation removed successfully!');
        window.location.href = "/officerDashboard";
      } 
    }
  };
  
  if (loading) { return <Loading />; }
  return (
      <form onSubmit={handleSubmit} className="remove-citation-form">
      <div className="form-header">
        <h1>Remove Citation</h1>
        <p>Enter Ticket ID Number and click Remove Citation:</p>
      </div>
      <div className="row0-remove-citation-form">
        <input name="ticketNumber" placeholder="Ticket ID Number" onChange={handleChange} value={removeTicketForm.ticketNumber} required />
      </div>
      <button type="submit" disabled={loading}>
        {loading ? 'Removing Citation...' : 'Remove Citation'}
      </button>
      </form>
    );
}

export default RemoveCitation;