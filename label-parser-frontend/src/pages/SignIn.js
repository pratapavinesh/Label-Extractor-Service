import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom'; // Import Link from react-router-dom
import { signin } from '../services/authService';
import './formStyles.css';

export default function SignIn() {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const navigate = useNavigate();

    const handleSubmit = async (event) => {
        event.preventDefault();
        try {
            const response = await signin(username, password);
            localStorage.setItem('token', response.data.token);
            localStorage.setItem('username', username);
            navigate('/dashboard');
        } catch (error) {
            try {
                alert('Login failed: ' + error.response.data.message);
            }
           catch (error){
            alert('Login failed: ');
           } 
        }
    };

    return (
        <div className="form-container">
            <form className="form-box" onSubmit={handleSubmit}>
                <input type="text" className="form-input" value={username} onChange={(e) => setUsername(e.target.value)} placeholder="Username" required />
                <input type="password" className="form-input" value={password} onChange={(e) => setPassword(e.target.value)} placeholder="Password" required />
                <button type="submit" className="form-button">Sign In</button>
                <p className="form-footer">
                    Don't have an account? <Link to="/signup">Sign Up</Link>
                </p>
            </form>
        </div>
    );
}