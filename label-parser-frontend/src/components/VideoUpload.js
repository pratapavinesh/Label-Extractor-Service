import React, { useState } from 'react';
import axios from 'axios';
import './videoUpload.css'

const VideoUpload = ({ token, username, onUploadComplete }) => {
    const [isLoading, setIsLoading] = useState(false);
    const [file, setFile] = useState(null);
    const [label, setLabel] = useState(null);
    const [inputKey, setInputKey] = useState(Date.now());

    const handleFileChange = (event) => {
        const selectedFile = event.target.files[0];
        if (!selectedFile) return;
        setFile(selectedFile);
        setLabel(null);
        setIsLoading(false);
    };

    const handleUploadAndExtract = async () => {
        if (!file) {
            alert("Please select a file first.");
            return;
        }
        setIsLoading(true);
        const formData = new FormData();
        formData.append('file', file);
        try {
            const response = await axios.post('http://localhost:5002/extract-labels', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data',
                    'Authorization': token,
                    'username': username,
                },
            });
            setLabel(response.data);  // Assuming the response includes the label data
            onUploadComplete(response.data.label);
        } catch (error) {
            console.error('Error uploading and extracting video:', error);
            alert('Error processing video');
        }
        setIsLoading(false);
    };

    const handleRefresh = () => {
        setInputKey(Date.now());
        setFile(null);
        setLabel(null);
        setIsLoading(false);
    };

    return (
        <div className="upload-box">
            <input type="file" key={inputKey} onChange={handleFileChange} accept="video/*" />
            {!isLoading && file && !label && (
                <button onClick={handleUploadAndExtract}>Upload and Extract Labels</button>
            )}
            {isLoading && <p>Processing...</p>}
            {label && (
                <div className="labels-container">
                    <div className="card">
                       <img src={`data:image/jpeg;base64,${label.image_data}`} alt={label.label_name} />
                        <h3 className="label-name">{label.label_name}</h3>
                        <p className="label-content">{label.image_content}</p>
                    </div>
                    <button onClick={handleRefresh} className="reset-button">Refresh</button>
                </div>
            )}
        </div>
    );
};

export default VideoUpload;
