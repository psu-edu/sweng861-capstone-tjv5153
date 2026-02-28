import React, {useState} from "react";
import './LicensePlate.css';
import { ApiClientPostFile } from "./ApiClient";

function LicensePlate() {
    const [selectedFile, setSelectedFile] = useState(null);
    const handleFileChange = (event) => {
    const file = event.target.files[0]; 
    setSelectedFile(file);
    console.log("File selected:", file);

    try {
        ApiClientPostFile("/checkLicensePlate", file)
            .then(response => {
                console.log("API response:", response);
                if (response.status === 200) {
                    window.location.href = "/accessGranted";
                } else if (response.status === 403) {
                    alert("Access denied! YOU DO NOT HAVE A VALID PARKING PASS.");
                } else {
                    alert("An unexpected error occurred. Please try again.");
                }
            })
            .catch(error => {
                console.error("Error uploading file:", error);
            });
    } catch (error) {
        console.error("Unexpected error:", error);
    }
  };

    return (
        <div className="license-plate-file-upload">
            <input type="file" onChange={handleFileChange} />
        {selectedFile && (
        <div>
          <h2>License Plate:</h2>
          <img src={URL.createObjectURL(selectedFile)} alt="preview" style={{ maxWidth: '300px', maxHeight: '300px' }} />
        </div>
      )}
    </div>
    );
}

export default LicensePlate;