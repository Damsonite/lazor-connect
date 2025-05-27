import { Send } from 'lucide-react-native';
import { useColorScheme } from 'nativewind';
import { TextInput, TouchableOpacity, View } from 'react-native';

import { colors, withOpacity } from '~/utils/colors';

interface ChatInputProps {
  inputMessage: string;
  setInputMessage: (text: string) => void;
  handleSendMessage: () => void;
  sendingMessage: boolean;
}

export default function ChatInput({
  inputMessage,
  setInputMessage,
  handleSendMessage,
  sendingMessage,
}: ChatInputProps) {
  const { colorScheme } = useColorScheme();
  const mode = colorScheme ?? 'light';

  return (
    <View className="mb-12 flex-row p-6 pt-2">
      <TextInput
        style={{
          color: colors.text[mode],
          backgroundColor: withOpacity('primary', 0.1, mode),
          borderColor: withOpacity('primary', 0.2, mode),
        }}
        className="mr-3 max-h-32 flex-1 rounded-3xl border p-4 font-itregular tracking-wider"
        value={inputMessage}
        onChangeText={setInputMessage}
        placeholder="Type a message..."
        placeholderTextColor={withOpacity('text', 0.5, mode)}
        multiline
      />
      <TouchableOpacity
        style={{
          backgroundColor: !inputMessage.trim()
            ? withOpacity('text', 0.2, mode)
            : colors.primary[mode],
        }}
        className="size-14 items-center justify-center rounded-full"
        onPress={handleSendMessage}
        disabled={!inputMessage.trim() || sendingMessage}>
        <Send size={20} color={colors.background[mode]} />
      </TouchableOpacity>
    </View>
  );
}
