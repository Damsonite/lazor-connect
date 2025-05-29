import { useRouter } from 'expo-router';
import { Plus } from 'lucide-react-native';
import { useColorScheme } from 'nativewind';
import { Text, TouchableOpacity, View } from 'react-native';

import ContactList from '~/components/contacts/ContactList';
import { colors } from '~/utils/colors';

export default function ContactSidebar() {
  const { colorScheme } = useColorScheme();
  const mode = colorScheme ?? 'light';
  const router = useRouter();

  return (
    <View className="flex-1">
      <View
        className="border-gray/20 border-b px-4 py-6"
        style={{
          backgroundColor: colors.background[mode],
          borderBottomColor: colors.gray[mode] + '33',
        }}>
        <View className="flex-row items-center justify-between">
          <Text className="font-orbitron text-lg" style={{ color: colors.primary[mode] }}>
            LazorConnect
          </Text>
          <TouchableOpacity
            onPress={() => router.push('/contact/create')}
            className="bg-primary/10 h-8 w-8 items-center justify-center rounded-full">
            <Plus color={colors.primary[mode]} size={24} />
          </TouchableOpacity>
        </View>
      </View>

      <ContactList isSidebar />
    </View>
  );
}
