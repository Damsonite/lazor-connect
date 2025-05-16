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

const getContacts = async (): Promise<Contact[]> => {
  try {
    const response = await api.get('/contacts');
    console.log('Contacts fetched:', response.data);

    // Transform the response data
    return response.data.map((contact: any) => ({
      id: contact.id,
      first_name: contact.first_name,
      last_name: contact.last_name,
      email: contact.email,
      phone_numbers: contact.phone_numbers?.map((p: any) => p.number) || [],
      company: contact.company,
      job_title: contact.job_title,
      contact_type: contact.contact_type,
      notes: contact.notes,
      favorite: contact.favorite,
      tags: contact.tags || [],
    }));
  } catch (error) {
    console.error('Error fetching contacts:', error);
    return [];
  }
};

const deleteContact = async (id: number): Promise<void> => {
  try {
    await api.delete(`/contacts/${id}`);
    console.log(`Contact with id ${id} deleted successfully`);
  } catch (error) {
    console.error(`Error deleting contact with id ${id}:`, error);
    throw error;
  }
};

const updateContact = async (id: number, contact: Partial<ContactCreate>): Promise<Contact> => {
  try {
    const payload = { ...contact };
    const response = await api.put(`/contacts/${id}`, payload);
    console.log('Contact updated:', response.data);

    // Return the updated contact
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
      tags: response.data.tags || [],
    };
  } catch (error) {
    console.error(`Error updating contact with id ${id}:`, error);
    throw error;
  }
};

const getContactById = async (id: number): Promise<Contact> => {
  try {
    const response = await api.get(`/contacts/${id}`);
    console.log(`Contact with id ${id} fetched:`, response.data);

    // Transform the response data
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
      tags: response.data.tags || [],
    };
  } catch (error) {
    console.error(`Error fetching contact with id ${id}:`, error);
    throw error;
  }
};

export { createContact, deleteContact, getContactById, getContacts, pingServer, updateContact };
