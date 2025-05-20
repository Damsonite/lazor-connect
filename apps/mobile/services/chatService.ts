import axios from 'axios';

import { Message } from '~/components/chat/MessageBubble';
import { Contact } from '~/types/contact';

const API_URL = process.env.EXPO_PUBLIC_API_URL;

const api = axios.create({
  baseURL: API_URL,
});

// Define interfaces for API responses
interface ChatResponse {
  contact_id: string;
  user_message: string;
  bot_response: string;
  contact_details: Contact;
  profile_suggestions?: Record<string, any>; // Structured data extracted from the conversation
}

interface GreetingResponse {
  contact_id: string;
  greeting: string;
  contact_details: Contact;
}

export const sendChatMessage = async (
  contactId: string,
  message: string
): Promise<ChatResponse> => {
  try {
    const response = await api.post<ChatResponse>(`/chat/${contactId}/send`, {
      message,
    });
    console.log(`Message sent to AI for contact ${contactId}:`, response.data);
    return response.data;
  } catch (error) {
    console.error(`Error sending message for contact ${contactId}:`, error);
    throw error;
  }
};

export const getInitialGreeting = async (contactId: string): Promise<GreetingResponse> => {
  try {
    const response = await api.get<GreetingResponse>(`/chat/${contactId}/greeting`);
    console.log(`Got greeting for contact ${contactId}:`, response.data);
    return response.data;
  } catch (error) {
    console.error(`Error getting greeting for contact ${contactId}:`, error);
    throw error;
  }
};

// Helper function to create message objects
export const createUserMessage = (text: string): Message => {
  return {
    id: Date.now().toString(),
    text,
    isUser: true,
    timestamp: new Date(),
  };
};

export const createBotMessage = (text: string): Message => {
  return {
    id: Date.now().toString(),
    text,
    isUser: false,
    timestamp: new Date(),
  };
};
