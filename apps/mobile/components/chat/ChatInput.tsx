import { Send } from 'lucide-react-native';
import { StyleSheet, TextInput, TouchableOpacity, View } from 'react-native';

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
    <View style={styles.inputContainer}>
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
    </View>
  );
}

const styles = StyleSheet.create({
  inputContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    padding: 16,
    paddingTop: 8,
    borderTopWidth: 1,
    borderTopColor: '#e0e0e0',
    backgroundColor: '#fff',
  },
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
