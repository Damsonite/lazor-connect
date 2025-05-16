import axios from 'axios';

import { Contact, ContactCreate } from '~/types/contact';

const API_URL = process.env.EXPO_PUBLIC_API_URL;

const api = axios.create({
  baseURL: API_URL,
});

const pingServer = async () => {
  try {
    const res = await api.get('/ping');
    console.log('Server response:', res.data);
    return res.data;
  } catch (error) {
    console.error('Error pinging server:', error);
    throw error;
  }
};

const createContact = async (contact: ContactCreate): Promise<Contact> => {
  try {
    const payload: ContactCreate = {
      first_name: contact.first_name,
      last_name: contact.last_name,
      email: contact.email,
      phone_numbers: contact.phone_numbers || [],
      company: contact.company,
      job_title: contact.job_title,
      notes: contact.notes,
      favorite: contact.favorite || false,
      tags: contact.tags || [],
    };

    const response = await api.post('/contacts', payload);
    console.log('Contact created:', response.data);

    // Return the created contact (transformed from snake_case to camelCase)
    return {
      id: response.data.id,
      first_name: response.data.first_name,
      last_name: response.data.last_name,
      email: response.data.email,
      phone_numbers: response.data.phone_numbers?.map((p: any) => p.number) || [],
      company: response.data.company,
      job_title: response.data.job_title,
      contact_type: response.data.contact_type,
      notes: response.data.notes,
      favorite: response.data.favorite,
      tags: response.data.tags,
    };
  } catch (error) {
    console.error('Error creating contact:', error);
    throw error;
  }
};

export { createContact, pingServer };
