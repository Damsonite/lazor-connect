import { useRouter } from 'expo-router';
import { User } from 'lucide-react-native';
import { Text, TouchableOpacity, View } from 'react-native';

import { Contact } from '~/types/contact';

export default function ContactItem({ contact }: { contact: Contact }) {
  const router = useRouter();

  const handlePress = () => {
    router.push({ pathname: '/contact/[id]', params: { id: String(contact.id) } });
  };

  return (
    <TouchableOpacity
      onPress={handlePress}
      className="flex-row items-center border-b border-gray-200 p-4">
      <View className="mr-4 h-12 w-12 items-center justify-center rounded-full bg-indigo-100">
        <User />
      </View>

      <Text className="flex-1 text-lg font-medium">{contact.name}</Text>
    </TouchableOpacity>
  );
}
