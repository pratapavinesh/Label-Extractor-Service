import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { signup } from '../services/authService';
import './formStyles.css';

export default function SignUp() {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const navigate = useNavigate();

    const handleSubmit = async (event) => {
        event.preventDefault();
        signup(username, password)
            .then(response => {
                navigate('/signin'); // Redirect to sign-in after successful sign-up
            })
            .catch(error => {
                // Check for error handling in the response
                const errorMessage = error.response && error.response.data ? error.response.data.message : 'Registration failed. Please try again.';
                alert(errorMessage);
            });
    };

    return (
        <div className="form-container">
            <form className="form-box" onSubmit={handleSubmit}>
                <input type="text" className="form-input" value={username} onChange={(e) => setUsername(e.target.value)} placeholder="Username" required />
                <input type="password" className="form-input" value={password} onChange={(e) => setPassword(e.target.value)} placeholder="Password" required />
                <button type="submit" className="form-button">Sign Up</button>
                <p className="form-footer">
                    Already have an account? <Link to="/signin">Sign In</Link>
                </p>
            </form>
        </div>
    );
}