import axios from 'axios';

import { Contact, ContactCreate } from '~/types/contact';

const API_URL = process.env.EXPO_PUBLIC_API_URL;

const api = axios.create({
  baseURL: API_URL,
});

const createContact = async (contact: ContactCreate) => {
  try {
    // Create payload with all fields from the contact
    const payload: ContactCreate = {
      name: contact.name,
      // Include all optional fields that exist in the contact object
      ...(contact.nickname && { nickname: contact.nickname }),
      ...(contact.birthday && { birthday: contact.birthday }),
      ...(contact.contact_methods && { contact_methods: contact.contact_methods }),
      ...(contact.relationship_type && { relationship_type: contact.relationship_type }),
      ...(contact.relationship_strength && {
        relationship_strength: contact.relationship_strength,
      }),
      ...(contact.conversation_topics && {
        conversation_topics: contact.conversation_topics,
      }),
      ...(contact.important_dates && {
        important_dates: contact.important_dates,
      }),
      ...(contact.reminders && {
        reminders: contact.reminders,
      }),
      ...(contact.interests && {
        interests: contact.interests,
      }),
      ...(contact.family_details && {
        family_details: contact.family_details,
      }),
      ...(contact.preferences && {
        preferences: contact.preferences,
      }),
      ...(contact.personality && {
        personality: contact.personality,
      }),
      ...(contact.last_connection && {
        last_connection: contact.last_connection,
      }),
      ...(contact.avg_days_btw_contacts && {
        avg_days_btw_contacts: contact.avg_days_btw_contacts,
      }),
      ...(contact.recommended_contact_freq_days && {
        recommended_contact_freq_days: contact.recommended_contact_freq_days,
      }),
    };

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
