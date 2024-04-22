import React, { useState, useEffect } from 'react';
import { getUserLabels, searchLabelsByName } from '../services/labelService';
import { useNavigate } from 'react-router-dom';
import './dashboard.css'; 
import VideoUpload from '../components/VideoUpload';

export default function Dashboard() {
    const [username, setUsername] = useState('');
    const [labels, setLabels] = useState([]);
    const [searchTerm, setSearchTerm] = useState('');
    const [isSearchActive, setIsSearchActive] = useState(false);
    const navigate = useNavigate();
    const [token, setToken] = useState('');

    useEffect(() => {
        setToken(localStorage.getItem('token'));
        const storedUsername = localStorage.getItem('username');
        if (storedUsername) {
            setUsername(storedUsername);
        } else {
            navigate('/signin');
        }
    }, [navigate]);

    useEffect(() => {
        if (username && !isSearchActive) {
            loadLabels();
        }
    }, [username, isSearchActive]);

    const loadLabels = async () => {
        const response = await getUserLabels(username);
        setLabels(response.data.labeled_images);
    };

    const handleSearch = async (event) => {
        event.preventDefault();
        if (searchTerm) {
            const response = await searchLabelsByName(username, searchTerm);
            setLabels(response.data.matching_labels);
            setIsSearchActive(true);
        }
    };

    const handleResetSearch = () => {
        setIsSearchActive(false);
    };

    const handleUploadComplete = () => {
        // You might want to fetch labels again or show results
        console.log("Upload complete, ready to extract labels!");
        loadLabels(); // Reload or refresh labels if needed
    };

    return (
        <div className="dashboard-container">
            {token && <VideoUpload token={token} username={username} onUploadComplete={handleUploadComplete} />}
            <div className="centered-flex">
                <div className="search-container">
                    <form onSubmit={handleSearch}>
                        <input type="text" className="search-input" value={searchTerm} onChange={(e) => setSearchTerm(e.target.value)} placeholder="Search labels by name" aria-label="Search Labels" />
                        <button type="submit" className="search-button">Search</button>
                    </form>
                </div>
            </div>
            {isSearchActive && (
                <div className="controls">
                    <button onClick={handleResetSearch} className="reset-button">Show All My Labels</button>
                </div>
            )}
            <div className="labels-container">
                {labels.map((label, index) => (
                    <div key={index} className="card">
                        <img src={`data:image/jpeg;base64,${label.image_data}`} alt={label.label_name} />
                        <h3 className="label-name">{label.label_name}</h3>
                        <p className="label-content">{label.image_content}</p>
                    </div>
                ))}
            </div>
        </div>
    );
}
