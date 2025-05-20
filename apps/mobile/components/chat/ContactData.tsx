import { Text, View } from 'react-native';

import { Contact } from '~/types/contact';

export default function ContactData({ contact }: { contact: Contact }) {
  return (
    <View className="border-b border-b-gray-200 bg-white p-4">
      <Text className="mb-4 text-3xl font-bold">{contact.name}</Text>
      <View className="flex-col gap-2">
        {contact.interests && contact.interests.length > 0 && (
          <View className="flex-col">
            <Text className="text-gray-500">Interests:</Text>
            <Text className="text-lg color-slate-800">{contact.interests.join(', ')}</Text>
          </View>
        )}
      </View>
    </View>
  );
}
