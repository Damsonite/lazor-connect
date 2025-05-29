import { Contact, ContactCreate } from '~/types/contact';

// Mock data for fallback mode
const MOCK_CONTACTS: Contact[] = [
  {
    id: '1',
    name: 'Alice Johnson',
    nickname: 'Ally',
    relationship_type: 'friend',
    relationship_strength: 4,
    interests: ['hiking', 'photography', 'reading'],
    last_connection: new Date(Date.now() - 86400000 * 3), // 3 days ago
    current_streak: 5,
    longest_streak: 12,
    recommended_contact_freq_days: 7,
    conversation_topics: ['travel', 'books', 'nature photography'],
    personality: 'Outgoing and adventurous, loves exploring new places',
    family_details: 'Has two younger siblings, close to her parents',
    preferences: {
      likes: ['coffee', 'mountains', 'indie music'],
      dislikes: ['crowded places', 'spicy food'],
    },
  },
  {
    id: '2',
    name: 'Bob Wilson',
    nickname: 'Bobby',
    relationship_type: 'colleague',
    relationship_strength: 3,
    interests: ['coding', 'gaming', 'cooking'],
    last_connection: new Date(Date.now() - 86400000 * 7), // 1 week ago
    current_streak: 1,
    longest_streak: 8,
    recommended_contact_freq_days: 14,
    conversation_topics: ['technology', 'video games', 'recipes'],
    personality: 'Quiet but friendly, very detail-oriented',
    family_details: 'Married with one daughter',
    preferences: {
      likes: ['Italian food', 'strategy games', 'clean code'],
      dislikes: ['meetings', 'loud environments'],
    },
  },
  {
    id: '3',
    name: 'Carmen Rodriguez',
    relationship_type: 'family',
    relationship_strength: 5,
    interests: ['gardening', 'cooking', 'family time'],
    last_connection: new Date(Date.now() - 86400000 * 1), // yesterday
    current_streak: 15,
    longest_streak: 25,
    recommended_contact_freq_days: 3,
    conversation_topics: ['family updates', 'recipes', 'garden tips'],
    personality: 'Warm and caring, always puts family first',
    family_details: 'Mother of three, grandmother of two',
    preferences: {
      likes: ['homemade meals', 'flowers', 'family gatherings'],
      dislikes: ['processed food', 'loud music'],
    },
  },
  {
    id: '4',
    name: 'David Chen',
    nickname: 'Dave',
    relationship_type: 'friend',
    relationship_strength: 4,
    interests: ['music', 'travel', 'food'],
    last_connection: new Date(Date.now() - 86400000 * 14), // 2 weeks ago
    current_streak: 0,
    longest_streak: 6,
    recommended_contact_freq_days: 10,
    conversation_topics: ['concerts', 'restaurants', 'travel stories'],
    personality: 'Enthusiastic and social, loves trying new experiences',
    family_details: 'Single, has a brother living abroad',
    preferences: {
      likes: ['live music', 'Asian cuisine', 'weekend trips'],
      dislikes: ['staying indoors', 'boring conversations'],
    },
  },
];

let mockContactsStore = [...MOCK_CONTACTS];

export const MockContactService = {
  // Get all contacts
  getContacts: async (): Promise<Contact[]> => {
    // Simulate API delay
    await new Promise((resolve) => setTimeout(resolve, 500));
    console.log('🔧 Using mock contact service - getContacts');
    return [...mockContactsStore];
  },

  // Get contact by ID
  getContactById: async (id: string): Promise<Contact> => {
    await new Promise((resolve) => setTimeout(resolve, 300));
    console.log(`🔧 Using mock contact service - getContactById: ${id}`);

    const contact = mockContactsStore.find((c) => c.id === id);
    if (!contact) {
      throw new Error(`Contact with id ${id} not found`);
    }
    return { ...contact };
  },

  // Create new contact
  createContact: async (contact: ContactCreate): Promise<Contact> => {
    await new Promise((resolve) => setTimeout(resolve, 400));
    console.log('🔧 Using mock contact service - createContact');

    const newContact: Contact = {
      id: Date.now().toString(),
      ...contact,
      current_streak: 0,
      longest_streak: 0,
      last_connection: undefined,
    };

    mockContactsStore.push(newContact);
    return { ...newContact };
  },

  // Update contact
  updateContact: async (id: string, updates: Partial<ContactCreate>): Promise<void> => {
    await new Promise((resolve) => setTimeout(resolve, 400));
    console.log(`🔧 Using mock contact service - updateContact: ${id}`);

    const index = mockContactsStore.findIndex((c) => c.id === id);
    if (index === -1) {
      throw new Error(`Contact with id ${id} not found`);
    }

    mockContactsStore[index] = {
      ...mockContactsStore[index],
      ...updates,
    };
  },

  // Delete contact
  deleteContact: async (id: string): Promise<void> => {
    await new Promise((resolve) => setTimeout(resolve, 300));
    console.log(`🔧 Using mock contact service - deleteContact: ${id}`);

    const index = mockContactsStore.findIndex((c) => c.id === id);
    if (index === -1) {
      throw new Error(`Contact with id ${id} not found`);
    }

    mockContactsStore.splice(index, 1);
  },

  // Reset to original mock data (useful for testing)
  resetMockData: () => {
    console.log('🔧 Resetting mock contact data');
    mockContactsStore = [...MOCK_CONTACTS];
  },

  // Check if we're in mock mode (always true for this service)
  isInMockMode: () => true,
};
