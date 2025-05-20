import { useState } from 'react';
import { Text, View } from 'react-native';

import ContactDetailField from './ContactDetailField';

import { Contact } from '~/types/contact';

export default function ContactData({ contact }: { contact: Contact }) {
  const [expanded, setExpanded] = useState(false);

  return (
    <View className="border-b border-b-gray-200 bg-white p-4">
      <View className="flex-row items-center justify-between">
        <View>
          <Text className="mb-2 text-3xl font-bold">{contact.name}</Text>
          {contact.nickname && <Text className="mb-2 text-lg italic">"{contact.nickname}"</Text>}
        </View>
        <Text
          className="px-2 py-1 text-base text-blue-500"
          onPress={() => setExpanded((prev) => !prev)}>
          {expanded ? 'Show less' : 'Show more'}
        </Text>
      </View>
      {expanded && (
        <View className="mt-2 flex-col gap-2">
          {contact.birthday && (
            <ContactDetailField label="Birthday">
              {new Date(contact.birthday).toLocaleDateString()}
            </ContactDetailField>
          )}

          {contact.relationship_type && (
            <ContactDetailField label="Relationship">
              {contact.relationship_type}
            </ContactDetailField>
          )}

          {contact.relationship_strength && (
            <ContactDetailField label="Connection strength">
              {contact.relationship_strength}/5
            </ContactDetailField>
          )}

          {contact.interests && contact.interests.length > 0 && (
            <ContactDetailField label="Interests" inline={false}>
              <Text className="text-md text-slate-800">{contact.interests.join(', ')}</Text>
            </ContactDetailField>
          )}

          {contact.conversation_topics && contact.conversation_topics.length > 0 && (
            <ContactDetailField label="Previous conversation topics" inline={false}>
              <Text className="text-md text-slate-800">
                {contact.conversation_topics.join(', ')}
              </Text>
            </ContactDetailField>
          )}

          {contact.last_connection && (
            <ContactDetailField label="Last contact">
              {new Date(contact.last_connection).toLocaleDateString()}
            </ContactDetailField>
          )}

          {contact.family_details && (
            <ContactDetailField label="Family details" inline={false}>
              <Text className="text-md text-slate-800">{contact.family_details}</Text>
            </ContactDetailField>
          )}

          {contact.personality && (
            <ContactDetailField label="Personality" inline={false}>
              <Text className="text-md text-slate-800">{contact.personality}</Text>
            </ContactDetailField>
          )}
        </View>
      )}
    </View>
  );
}
