import axios from 'axios';

import { ChatResponse, GreetingResponse, Message } from '~/types/chat';

const API_URL = process.env.EXPO_PUBLIC_API_URL;

const api = axios.create({
  baseURL: API_URL,
  timeout: 30000, // Increase timeout to 30 seconds
});

export const sendChatMessage = async (
  contactId: string,
  message: string
): Promise<ChatResponse> => {
  try {
    const response = await api.post<ChatResponse>(`/chat/${contactId}/send`, {
      message,
    });
    console.log(`Message sent to AI for contact ${contactId}:`, response.data);

    // Validate response data
    if (!response.data.bot_response) {
      console.warn(
        `Bot response is missing or null for contact ${contactId}. Using fallback message.`
      );
      response.data.bot_response = "I'm sorry, I couldn't process your message. Please try again.";
    }

    if (!response.data.profile_suggestions) {
      response.data.profile_suggestions = {};
    }

    return response.data;
  } catch (error) {
    // More detailed error logging
    if (axios.isAxiosError(error)) {
      console.error(`Error sending message for contact ${contactId}:`, {
        message: error.message,
        status: error.response?.status,
        data: error.response?.data,
      });
    } else {
      console.error(`Error sending message for contact ${contactId}:`, error);
    }
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
