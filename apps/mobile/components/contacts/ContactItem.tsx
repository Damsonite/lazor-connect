import { useRouter } from 'expo-router';
import { Briefcase, Mail, Phone, Star } from 'lucide-react-native';
import { Text, TouchableOpacity, View } from 'react-native';

import { Contact } from '~/types/contact';

interface ContactItemProps {
  contact: Contact;
}

export default function ContactItem({ contact }: ContactItemProps) {
  const router = useRouter();

  const getInitials = () => {
    return `${contact.first_name.charAt(0)}${contact.last_name.charAt(0)}`.toUpperCase();
  };

  const handlePress = () => {
    // Navigate to the contact details page (to be implemented)
    // router.push(`/contact/${contact.id}`);
    console.log('Contact pressed:', contact);
  };

  return (
    <TouchableOpacity
      onPress={handlePress}
      className="flex-row items-center border-b border-gray-200 p-4">
      <View className="mr-4 h-12 w-12 items-center justify-center rounded-full bg-indigo-100">
        <Text className="text-lg font-bold text-indigo-600">{getInitials()}</Text>
      </View>

      <View className="flex-1">
        <View className="flex-row items-center">
          <Text className="flex-1 text-lg font-medium">
            {contact.first_name} {contact.last_name}
          </Text>
          {contact.favorite && <Star size={16} color="#F59E0B" fill="#F59E0B" />}
        </View>

        {contact.company && (
          <View className="mt-1 flex-row items-center">
            <Briefcase size={14} color="#6B7280" />
            <Text className="ml-1 text-sm text-gray-500">
              {contact.job_title ? `${contact.job_title}, ` : ''}
              {contact.company}
            </Text>
          </View>
        )}

        {contact.email && (
          <View className="mt-1 flex-row items-center">
            <Mail size={14} color="#6B7280" />
            <Text className="ml-1 text-sm text-gray-500">{contact.email}</Text>
          </View>
        )}

        {contact.phone_numbers && contact.phone_numbers.length > 0 && (
          <View className="mt-1 flex-row items-center">
            <Phone size={14} color="#6B7280" />
            <Text className="ml-1 text-sm text-gray-500">{contact.phone_numbers[0]}</Text>
          </View>
        )}
      </View>
    </TouchableOpacity>
  );
}
