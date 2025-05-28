import { useRouter } from 'expo-router';
import { Flame, User } from 'lucide-react-native';
import { useColorScheme } from 'nativewind';
import { Text, TouchableOpacity, View } from 'react-native';

import { Contact } from '~/types/contact';
import { colors, withOpacity } from '~/utils/colors';
import { formatRelativeTime } from '~/utils/date';

export default function ContactItem({ contact }: { contact: Contact }) {
  const router = useRouter();
  const { colorScheme } = useColorScheme();
  const mode = colorScheme ?? 'light';

  const streakColor = contact.current_streak ? colors.accent[mode] : withOpacity('text', 0.5, mode);

  const handlePress = () => {
    router.push({
      pathname: '/contact/[id]',
      params: { id: String(contact.id), name: contact.name },
    });
  };

  return (
    <TouchableOpacity onPress={handlePress} className="mb-4 flex-row items-center pr-2">
      <View
        className="mr-4 h-16 w-16 items-center justify-center rounded-xl"
        style={{
          backgroundColor: withOpacity('primary', 0.1, mode),
        }}>
        <User size={32} color={withOpacity('text', 0.75, mode)} />
      </View>

      <View className="flex-1">
        <Text className="font-exmedium text-lg text-text">{contact.name}</Text>

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
