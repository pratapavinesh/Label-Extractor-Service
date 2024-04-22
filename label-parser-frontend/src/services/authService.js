import axios from 'axios';

const API_URL = 'http://localhost:5000/'; // Adjust this URL to the location of your login service

export const signup = (username, password) => {
    return axios.post(`${API_URL}signup`, {
        username,
        password
    });
};

export const signin = (username, password) => {
    return axios.post(`${API_URL}signin`, {
        username,
        password
    });
};

export const checkConnection = () => {
    return axios.get(`${API_URL}check_connection`);
};
