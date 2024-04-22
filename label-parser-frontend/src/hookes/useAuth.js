import axios from 'axios';

const API_URL = 'http://localhost:5000/'; // Adjust if your login service is at a different port

export const signup = (username, password) => axios.post(`${API_URL}signup`, { username, password });
export const signin = (username, password) => axios.post(`${API_URL}signin`, { username, password });
