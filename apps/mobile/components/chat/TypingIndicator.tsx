import { useColorScheme } from 'nativewind';
import { ActivityIndicator, Text, View } from 'react-native';

import { colors } from '~/utils/colors';

export interface TypingIndicatorType {
  id: string;
  isTyping: boolean;
}

interface TypingIndicatorProps {
  typingIndicator: TypingIndicatorType | null;
}

export default function TypingIndicator({ typingIndicator }: TypingIndicatorProps) {
  const { colorScheme } = useColorScheme();
  const mode = colorScheme ?? 'light';

  if (!typingIndicator) return null;

  return (
    <View className="border-gray flex-row border-t bg-secondary px-4 py-2">
      <ActivityIndicator size="small" color={colors.primary[mode]} />
      <Text className="ml-2 font-itregular text-primary">AI is typing...</Text>
    </View>
  );
}
