import { ActivityIndicator, StyleSheet, Text, View } from 'react-native';

export interface TypingIndicatorType {
  id: string;
  isTyping: boolean;
}

interface TypingIndicatorProps {
  typingIndicator: TypingIndicatorType | null;
}

export default function TypingIndicator({ typingIndicator }: TypingIndicatorProps) {
  if (!typingIndicator) return null;

  return (
    <View style={styles.typingIndicator}>
      <ActivityIndicator size="small" color="#6366f1" />
      <Text style={styles.typingText}>AI is typing...</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  typingIndicator: {
    flexDirection: 'row',
    alignItems: 'center',
    padding: 8,
    paddingHorizontal: 16,
    borderTopWidth: 1,
    borderTopColor: '#e0e0e0',
    backgroundColor: '#fff',
  },
  typingText: {
    fontSize: 14,
    color: '#888',
    marginLeft: 8,
  },
});
