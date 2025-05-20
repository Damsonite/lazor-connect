interface ContactBase {
  // Basic contact information
  name: string;
  nickname?: string;
  birthday?: string;
  contact_methods?: {
    type: string; // e.g., 'presential', 'phone', 'social_media'
    value: string; // e.g., 'cinema', '123-456-7890', '@username'
    preferred?: boolean;
  }[];

  // Relationship management fields
  last_connection?: Date;
  avg_days_btw_contacts?: number;
  recommended_contact_freq_days?: number;
  relationship_type?: string; // e.g., 'friend', 'family', 'colleague'
  relationship_strength?: number; // 1-5

  // Contextual informations
  conversation_topics?: string[]; // e.g., 'movies', 'sports'
  important_dates?: { date: Date; description: string }[];
  reminders?: { text: string; due_date?: Date }[];

  // Personal details
  interests?: string[]; // e.g., 'hiking', 'reading'
  family_details?: string; // e.g., 'has a dog named Max'
  preferences?: { likes?: string[]; dislikes?: string[] }; // e.g., 'likes chocolate', 'dislikes broccoli'
  personality?: string; // Information about contact's personality, emotions, traits, etc.
}

interface Contact extends ContactBase {
  id: string; // Changed from number to string for UUID compatibility
}

interface ContactCreate extends ContactBase {}

export { Contact, ContactCreate };
