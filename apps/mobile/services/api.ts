import axios from 'axios';

const API_BASE_URL = 'http://YOUR_LOCAL_MACHINE_IP:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
});

export const pingServer = async () => {
  try {
    const res = await api.get('/ping');
    console.log('Server response:', res.data);
    return res.data;
  } catch (error) {
    console.error('Error pinging server:', error);
    throw error;
  }
};
