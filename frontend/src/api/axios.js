import axios from 'axios';

export const instance = axios.create({
    baseURL: import.meta.env.VITE_API_BASE_URL,
    timeout: 60000,
    headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
    },
});

instance.interceptors.request.use((config) => {
    const token = localStorage.getItem('session_token');
    if (token) config.headers['X-Session-Token'] = token;
    return config;
});

instance.interceptors.response.use(
    (response) => {
        return response;
    },
    (error) => {
        if (error.response) {
          throw new Error(`An error occured on the server: ${error.response.data.message}, ${error.response.status}`)
        } else if (error.request) {
          throw new Error(`Couldn't reach the server: ${error.request}`)
        } else {
          throw new Error(`An unknown error occured: ${error.message}`)
        }
    }
)