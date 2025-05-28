import { useRouter } from 'expo-router';
import { Flame, User } from 'lucide-react-native';
import { useColorScheme } from 'nativewind';
import { Text, TouchableOpacity, View } from 'react-native';

import { useSelectedContact } from '~/context/SelectedContactProvider';
import { Contact } from '~/types/contact';
import { colors, withOpacity } from '~/utils/colors';
import { formatRelativeTime } from '~/utils/date';

interface ContactItemProps {
  contact: Contact;
  isSidebar?: boolean;
}

export default function ContactItem({ contact, isSidebar = false }: ContactItemProps) {
  const router = useRouter();
  const { colorScheme } = useColorScheme();
  const mode = colorScheme ?? 'light';
  const { selectedContactId, setSelectedContactId } = useSelectedContact();

  const streakColor = contact.current_streak ? colors.accent[mode] : withOpacity('text', 0.5, mode);
  const isSelected = selectedContactId === String(contact.id);

  const handlePress = () => {
    const contactId = String(contact.id);
    setSelectedContactId(contactId);
    router.push({
      pathname: '/contact/[id]',
      params: { id: contactId, name: contact.name },
    });
  };

  return (
    <TouchableOpacity
      onPress={handlePress}
      className="mb-4 flex-row items-center rounded-xl"
      style={isSelected ? { backgroundColor: withOpacity('primary', 0.05, mode) } : {}}>
      <View
        className={`mr-4 items-center justify-center rounded-xl ${isSidebar ? 'size-12' : 'size-14'}`}
        style={{
          backgroundColor: withOpacity('primary', 0.1, mode),
        }}>
        <User size={32} color={withOpacity('text', 0.75, mode)} />
      </View>

      <View className="flex-1">
        <Text className={`font-exmedium text-text ${isSidebar ? 'text-base' : 'text-lg'}`}>
          {contact.name}
        </Text>

        <View className="mt-1 flex-row items-center gap-1 font-exsemibold">
          <Flame size={16} color={streakColor} />
          <Text
            className="mt-1 font-itmedium text-sm"
            style={{
              color: streakColor,
            }}>
            {contact.current_streak || 0}
          </Text>
        </View>
      </View>

      <View className="h-full justify-center">
        <Text className="font-itregular text-sm" style={{ color: withOpacity('text', 0.5, mode) }}>
          {contact.last_connection ? formatRelativeTime(contact.last_connection) : 'Unconnected'}
        </Text>
      </View>
    </TouchableOpacity>
  );
}
