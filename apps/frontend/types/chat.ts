import { Contact } from './contact';

/**
 * Response from the API when sending a chat message
 */
export interface ChatResponse {
  contact_id: string;
  user_message: string;
  bot_response: string;
  contact_details: Contact;
  profile_suggestions?: Record<string, any>; // Structured data extracted from the conversation
}

/**
 * Response from the API when requesting an initial greeting
 */
export interface GreetingResponse {
  contact_id: string;
  greeting: string;
  contact_details: Contact;
}

/**
 * Message object used in the chat UI
 */
export interface Message {
  id: string;
  text: string;
  isUser: boolean;
  timestamp: Date;
}
