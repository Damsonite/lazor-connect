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
    <View className="flex-row p-4">
      <TextInput
        className="mr-3 h-12 flex-1 rounded-3xl border border-gray bg-secondary p-4 font-itregular tracking-wider text-text"
        value={inputMessage}
        onChangeText={setInputMessage}
        placeholder="Type a message..."
        placeholderTextColor={withOpacity('text', 0.5, mode)}
        multiline
      />
      <TouchableOpacity
        className={`size-12 items-center justify-center rounded-full border border-gray ${!inputMessage.trim() ? 'bg-gray' : 'bg-primary'}`}
        onPress={handleSendMessage}
        disabled={!inputMessage.trim() || sendingMessage}>
        <Send size={20} color={colors.background[mode]} />
      </TouchableOpacity>
    </View>
  );
}
