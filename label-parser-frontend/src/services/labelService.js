import axios from 'axios';

const API_URL = 'http://localhost:5001/'; // Adjust if your label service is at a different port

// Configure Axios to include the JWT in all requests
axios.interceptors.request.use((config) => {
    const token = localStorage.getItem('token');
    config.headers.Authorization = token ? `${token}` : '';
    return config;
});

export const getUserLabels = (username) => axios.get(`${API_URL}get-user-labels`, { params: { username } });
export const searchLabelsByName = (username, labelName) => axios.get(`${API_URL}search-labels`, {
    params: {
        username,
        labelName
    }
});
export const createLabel = (data) => axios.post(`${API_URL}create-label`, data);
