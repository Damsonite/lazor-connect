import axios from 'axios';

const API_URL = process.env.EXPO_PUBLIC_API_URL;

const api = axios.create({
  baseURL: API_URL,
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
