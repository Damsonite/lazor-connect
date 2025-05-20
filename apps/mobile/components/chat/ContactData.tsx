import { Text, View } from 'react-native';

import { Contact } from '~/types/contact';

export default function ContactData({ contact }: { contact: Contact }) {
  return (
    <View className="border-b border-b-gray-200 bg-white p-4">
      <Text className="mb-2 text-3xl font-bold">{contact.name}</Text>
      {contact.nickname && <Text className="mb-2 text-lg italic">"{contact.nickname}"</Text>}

      <View className="mt-2 flex-col gap-2">
        {contact.relationship_type && (
          <View className="mb-1 flex-row">
            <Text className="mr-1 text-gray-500">Relationship:</Text>
            <Text className="text-md text-slate-800">{contact.relationship_type}</Text>
          </View>
        )}

        {contact.relationship_strength && (
          <View className="mb-1 flex-row">
            <Text className="mr-1 text-gray-500">Connection strength:</Text>
            <Text className="text-md text-slate-800">{contact.relationship_strength}/5</Text>
          </View>
        )}

        {contact.interests && contact.interests.length > 0 && (
          <View className="mb-1 flex-col">
            <Text className="text-gray-500">Interests:</Text>
            <Text className="text-md text-slate-800">{contact.interests.join(', ')}</Text>
          </View>
        )}

        {contact.conversation_topics && contact.conversation_topics.length > 0 && (
          <View className="mb-1 flex-col">
            <Text className="text-gray-500">Previous conversation topics:</Text>
            <Text className="text-md text-slate-800">{contact.conversation_topics.join(', ')}</Text>
          </View>
        )}

        {contact.last_connection && (
          <View className="mb-1 flex-row">
            <Text className="mr-1 text-gray-500">Last contact:</Text>
            <Text className="text-md text-slate-800">
              {new Date(contact.last_connection).toLocaleDateString()}
            </Text>
          </View>
        )}
      </View>
    </View>
  );
}
