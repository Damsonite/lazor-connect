import axios from 'axios';

import { Contact, ContactCreate } from '~/types/contact';

const API_URL = process.env.EXPO_PUBLIC_API_URL;

const api = axios.create({
  baseURL: API_URL,
});

const createContact = async (contact: ContactCreate) => {
  try {
    // Filter out undefined values and send only defined fields
    const payload = Object.fromEntries(
      Object.entries(contact).filter(([_, value]) => value !== undefined && value !== null)
    );

    const response = await api.post('/contacts', payload);
    console.log('Contact created:', response.data);
    return response.data;
  } catch (error) {
    console.error('Error creating contact:', error);
    throw error;
  }
};

const getContacts = async (): Promise<Contact[]> => {
  try {
    const response = await api.get('/contacts');

    // Return the complete contact objects directly
    return response ? response.data : [];
  } catch (error) {
    console.error('Error fetching contacts:', error);
    return [];
  }
};

const deleteContact = async (id: Contact['id']) => {
  try {
    await api.delete(`/contacts/${id}`);
    console.log(`Contact with id ${id} deleted successfully`);
  } catch (error) {
    console.error(`Error deleting contact with id ${id}:`, error);
    throw error;
  }
};

const updateContact = async (id: Contact['id'], contact: Partial<ContactCreate>) => {
  try {
    const payload = { ...contact };
    const response = await api.put(`/contacts/${id}`, payload);
    console.log('Contact updated:', response.data);
  } catch (error) {
    console.error(`Error updating contact with id ${id}:`, error);
    throw error;
  }
};

const getContactById = async (id: Contact['id']): Promise<Contact> => {
  try {
    const response = await api.get<Contact>(`/contacts/${id}`);
    console.log(`Contact with id ${id} fetched:`, response.data);

    // Return the complete contact object directly
    return response.data;
  } catch (error) {
    console.error(`Error fetching contact with id ${id}:`, error);
    throw error;
  }
};

export { createContact, deleteContact, getContactById, getContacts, updateContact };
