import axios from 'axios';

import { Contact, ContactCreate } from '~/types/contact';

const API_URL = process.env.EXPO_PUBLIC_API_URL;

const api = axios.create({
  baseURL: API_URL,
  timeout: 10000, // 10 second timeout
});

// Helper function to check if we should use mock service
const shouldUseMockService = (error: any): boolean => {
  // Use mock service if:
  // 1. Network error (no internet, server down)
  // 2. Timeout error
  // 3. 5xx server errors (but not 4xx client errors)
  if (axios.isAxiosError(error)) {
    return (
      !error.response || // Network error
      error.code === 'ECONNABORTED' || // Timeout
      error.code === 'NETWORK_ERROR' ||
      error.response.status >= 500 // Server error
    );
  }
  return false;
};

// Helper function to call backend mock endpoints
const callMockEndpoint = async (
  endpoint: string,
  method: 'GET' | 'POST' | 'PUT' | 'DELETE' = 'GET',
  data?: any
) => {
  try {
    const config = {
      method,
      url: `/contacts/mock${endpoint}`,
      timeout: 5000, // Shorter timeout for mock endpoints
      ...(data && { data }),
    };
    const response = await api(config);
    return response.data;
  } catch (mockError) {
    console.error('Mock endpoint also failed:', mockError);
    throw new Error('Both primary API and mock endpoints are unavailable');
  }
};

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

    // Check if we should fallback to mock service
    if (shouldUseMockService(error)) {
      console.warn('⚠️ API unavailable, falling back to backend mock service');
      return await callMockEndpoint('', 'POST', contact);
    }

    throw error;
  }
};

const getContacts = async (): Promise<Contact[]> => {
  console.log('🔍 Attempting to fetch contacts list');
  try {
    const response = await api.get('/contacts');
    console.log('✅ Contacts fetched from main API:', response.data?.length || 0, 'contacts');

    // Return the complete contact objects directly
    return response ? response.data : [];
  } catch (error) {
    console.error('❌ Error fetching contacts from main API:', error);

    // Check if we should fallback to mock service
    if (shouldUseMockService(error)) {
      console.warn('⚠️ API unavailable, falling back to backend mock service');
      try {
        const mockData = await callMockEndpoint('');
        console.log('✅ Contacts fetched from mock API:', mockData?.length || 0, 'contacts');
        return mockData;
      } catch (mockError) {
        console.error('❌ Mock API also failed for contacts:', mockError);
        return [];
      }
    }

    // For client errors (4xx), return empty array instead of crashing
    return [];
  }
};

const deleteContact = async (id: Contact['id']) => {
  try {
    await api.delete(`/contacts/${id}`);
    console.log(`Contact with id ${id} deleted successfully`);
  } catch (error) {
    console.error(`Error deleting contact with id ${id}:`, error);

    // Check if we should fallback to mock service
    if (shouldUseMockService(error)) {
      console.warn('⚠️ API unavailable, falling back to backend mock service');
      return await callMockEndpoint(`/${id}`, 'DELETE');
    }

    throw error;
  }
};

const updateContact = async (id: Contact['id'], contact: Partial<ContactCreate>) => {
  try {
    const payload = { ...contact };
    const response = await api.put(`/contacts/${id}`, payload);
    console.log('Contact updated:', response.data);
    return response.data;
  } catch (error) {
    console.error(`Error updating contact with id ${id}:`, error);

    // Check if we should fallback to mock service
    if (shouldUseMockService(error)) {
      console.warn('⚠️ API unavailable, falling back to backend mock service');
      return await callMockEndpoint(`/${id}`, 'PUT', contact);
    }

    throw error;
  }
};

const getContactById = async (id: Contact['id']): Promise<Contact> => {
  console.log(`🔍 Attempting to fetch contact with id: ${id}`);
  try {
    const response = await api.get<Contact>(`/contacts/${id}`);
    console.log(`✅ Contact with id ${id} fetched from main API:`, response.data);

    // Return the complete contact object directly
    return response.data;
  } catch (error) {
    console.error(`❌ Error fetching contact with id ${id} from main API:`, error);

    // Check if we should fallback to mock service
    if (shouldUseMockService(error)) {
      console.warn('⚠️ API unavailable, falling back to backend mock service');
      try {
        const mockData = await callMockEndpoint(`/${id}`);
        console.log(`✅ Contact with id ${id} fetched from mock API:`, mockData);
        return mockData;
      } catch (mockError) {
        console.error(`❌ Mock API also failed for contact ${id}:`, mockError);
        throw mockError;
      }
    }

    throw error;
  }
};

export { createContact, deleteContact, getContactById, getContacts, updateContact };
