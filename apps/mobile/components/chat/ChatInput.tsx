import { Send } from 'lucide-react-native';
import {
  KeyboardAvoidingView,
  Platform,
  StyleSheet,
  TextInput,
  TouchableOpacity,
} from 'react-native';

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
  return (
    <KeyboardAvoidingView
      className="mb-8 flex-row bg-background p-6 pt-2"
      behavior={Platform.OS === 'ios' ? 'padding' : 'height'}>
      <TextInput
        style={styles.input}
        value={inputMessage}
        onChangeText={setInputMessage}
        placeholder="Type a message..."
        multiline
      />
      <TouchableOpacity
        style={[styles.sendButton, !inputMessage.trim() && styles.sendButtonDisabled]}
        onPress={handleSendMessage}
        disabled={!inputMessage.trim() || sendingMessage}>
        <Send size={20} color={inputMessage.trim() ? '#fff' : '#aaa'} />
      </TouchableOpacity>
    </KeyboardAvoidingView>
  );
}

const styles = StyleSheet.create({
  input: {
    flex: 1,
    borderWidth: 1,
    borderColor: '#e0e0e0',
    borderRadius: 24,
    padding: 12,
    paddingTop: 12,
    maxHeight: 120,
    marginRight: 12,
    backgroundColor: '#f9f9f9',
  },
  sendButton: {
    width: 44,
    height: 44,
    borderRadius: 22,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#6366f1',
  },
  sendButtonDisabled: {
    backgroundColor: '#e0e0e0',
  },
});
