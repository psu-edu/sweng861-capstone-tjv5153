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
            {selectedFile && <p>Selected file: {selectedFile.name}</p>}
        </div>
    );
}

export default LicensePlate;