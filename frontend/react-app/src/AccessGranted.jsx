import React from "react";
import './AccessGranted.css';

function AccessGranted() {
    return (
        <div className="access-granted-container" role="main" aria-live="polite">
            <div className="access-card">
                <div className="status">
                    <svg
                        className="check-icon"
                        width="48"
                        height="48"
                        viewBox="0 0 24 24"
                        fill="none"
                        xmlns="http://www.w3.org/2000/svg"
                        aria-hidden="true"
                        color="green"
                    >
                        <circle cx="12" cy="12" r="11" stroke="currentColor" strokeWidth="2" />
                        <path d="M7 12.5l2.5 2.5L17 8" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
                    </svg>
                    <h1 className="title">Access Granted</h1>
                </div>

                <p className="message">
                    Welcome to Penn State Campus! You may enter the parking garage when the gate is open.
                </p>

                <p className="note">Please have your permit visible and follow posted signage.</p>
            </div>
        </div>
    );
}

export default AccessGranted;