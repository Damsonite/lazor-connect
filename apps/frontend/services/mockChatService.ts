import axios from 'axios';

import { ChatResponse, GreetingResponse } from '~/types/chat';
import { Contact } from '~/types/contact';

const API_URL = process.env.EXPO_PUBLIC_API_URL;

const api = axios.create({
  baseURL: API_URL,
  timeout: 5000,
});

// Mock responses for different contact scenarios
const MOCK_RESPONSES = {
  // Generic responses for different relationship types
  friend: [
    "That sounds great! I'd love to hear more about how things are going with them.",
    "It's always nice to stay connected with good friends. What's new in their world?",
    'Friends like that are really special. I hope you two get to catch up soon!',
  ],
  family: [
    "Family is so important. I'm glad you're staying in touch with them.",
    "That's wonderful! Family connections really make a difference in our lives.",
    'It sounds like you have a great relationship. Family bonds are really precious.',
  ],
  colleague: [
    'Professional relationships can really enrich our work experience.',
    "It's great when we can connect with colleagues beyond just work topics.",
    'Building good relationships at work makes everything more enjoyable.',
  ],
  default: [
    "That's really nice to hear! Maintaining connections is so important.",
    "I'm glad you're taking the time to stay connected with people who matter to you.",
    'Relationships like this really make life more meaningful.',
  ],
};

const MOCK_GREETINGS = {
  friend: [
    'Hey! How are things going with {name}? I remember they love {interest}. Maybe you could ask about that!',
    "It's been a while since you connected with {name}! They might appreciate hearing from you.",
    'I remember {name} is really into {interest}. That could be a great conversation starter!',
  ],
  family: [
    'Family time is so important! How has {name} been doing lately?',
    'It would be great to catch up with {name}. Family connections are really special.',
    'I bet {name} would love to hear from you! Family bonds are so precious.',
  ],
  colleague: [
    "How are things going with {name} at work? It's nice to maintain professional relationships.",
    "Maybe it's time for a coffee chat with {name}? Workplace friendships are valuable.",
    'I remember {name} is great to work with. Building professional relationships is so important.',
  ],
  default: [
    "Hello! I'm here to help you stay connected with {name}. What would you like to know about them?",
    "Hi there! Let's think about {name} - what's the best way to connect with them today?",
    'Great to see you thinking about {name}! Maintaining relationships is so important.',
  ],
};

export const MockChatService = {
  // Send chat message
  sendChatMessage: async (contactId: string, message: string): Promise<ChatResponse> => {
    await new Promise((resolve) => setTimeout(resolve, 1000 + Math.random() * 1500)); // Simulate AI processing
    console.log(`🔧 Using mock chat service - sendChatMessage for contact: ${contactId}`);

    // Try to get contact info to personalize response
    let contact: Contact | null = null;
    try {
      // Get contact from backend mock service
      const response = await api.get(`/contacts/mock/${contactId}`);
      contact = response.data;
    } catch {
      console.log('Could not get contact for mock response, using generic response');
    }

    const relationshipType = contact?.relationship_type || 'default';
    const responses =
      MOCK_RESPONSES[relationshipType as keyof typeof MOCK_RESPONSES] || MOCK_RESPONSES.default;
    const randomResponse = responses[Math.floor(Math.random() * responses.length)];

    // Create mock profile suggestions based on the message
    const profileSuggestions: Record<string, any> = {};

    // Simple keyword detection for demo purposes
    if (message.toLowerCase().includes('birthday') || message.toLowerCase().includes('born')) {
      profileSuggestions.birthday = 'Consider asking about their birthday';
    }
    if (message.toLowerCase().includes('hobby') || message.toLowerCase().includes('like')) {
      profileSuggestions.interests = ['Ask about their hobbies and interests'];
    }
    if (message.toLowerCase().includes('family')) {
      profileSuggestions.family_details = 'Learn more about their family';
    }

    return {
      contact_id: contactId,
      user_message: message,
      bot_response: randomResponse,
      contact_details:
        contact ||
        ({
          id: contactId,
          name: 'Unknown Contact',
        } as Contact),
      profile_suggestions: profileSuggestions,
    };
  },

  // Get initial greeting
  getInitialGreeting: async (contactId: string): Promise<GreetingResponse> => {
    await new Promise((resolve) => setTimeout(resolve, 800));
    console.log(`🔧 Using mock chat service - getInitialGreeting for contact: ${contactId}`);

    // Try to get contact info to personalize greeting
    let contact: Contact | null = null;
    try {
      const response = await api.get(`/contacts/mock/${contactId}`);
      contact = response.data;
    } catch {
      console.log('Could not get contact for mock greeting, using generic greeting');
    }

    const relationshipType = contact?.relationship_type || 'default';
    const greetings =
      MOCK_GREETINGS[relationshipType as keyof typeof MOCK_GREETINGS] || MOCK_GREETINGS.default;
    let randomGreeting = greetings[Math.floor(Math.random() * greetings.length)];

    // Personalize the greeting
    if (contact) {
      randomGreeting = randomGreeting
        .replace('{name}', contact.name)
        .replace('{interest}', contact.interests?.[0] || 'their hobbies');
    } else {
      randomGreeting = randomGreeting
        .replace('{name}', 'this person')
        .replace('{interest}', 'their interests');
    }

    return {
      contact_id: contactId,
      greeting: randomGreeting,
      contact_details:
        contact ||
        ({
          id: contactId,
          name: 'Unknown Contact',
        } as Contact),
    };
  },

  // Check if we're in mock mode (always true for this service)
  isInMockMode: () => true,
};
