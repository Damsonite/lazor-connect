import { User } from 'lucide-react-native';
import { Alert, StyleSheet, Text, View } from 'react-native';
import {
  GestureHandlerRootView,
  LongPressGestureHandler,
  State,
} from 'react-native-gesture-handler';

import { submitFeedback } from '~/services/feedbackService';
import { Message } from '~/types/chat';

export interface MessageBubbleProps {
  message: Message;
  contactId: string;
}

export default function MessageBubble({ message, contactId }: MessageBubbleProps) {
  const handleLongPress = () => {
    if (!message.isUser) {
      Alert.alert(
        'Mark as Bad Response',
        'Do you want to mark this message as a bad response?',
        [
          {
            text: 'Cancel',
            style: 'cancel',
          },
          {
            text: 'Mark as Bad',
            onPress: async () => {
              try {
                await submitFeedback({
                  type: 'bad_response',
                  message_text: message.text,
                  message_id: message.id,
                  contact_id: contactId,
                  category: 'bad_ai_response',
                });
                Alert.alert('Feedback Submitted', 'Thank you for your feedback!');
              } catch (error) {
                console.error('Failed to submit feedback:', error);
                Alert.alert('Error', 'Failed to submit feedback. Please try again.');
              }
            },
            style: 'destructive',
          },
        ],
        { cancelable: true }
      );
    }
  };

  return (
    <GestureHandlerRootView>
      <LongPressGestureHandler
        onHandlerStateChange={({ nativeEvent }) => {
          if (nativeEvent.state === State.ACTIVE) {
            handleLongPress();
          }
        }}
        minDurationMs={800}>
        <View
          style={[
            styles.messageBubble,
            message.isUser ? styles.userMessageBubble : styles.aiMessageBubble,
          ]}>
          {!message.isUser && (
            <View style={styles.avatarContainer}>
              <View style={styles.avatar}>
                <User size={16} color="#fff" />
              </View>
            </View>
          )}
          <View
            style={[
              styles.messageContent,
              message.isUser ? styles.userMessageContent : styles.aiMessageContent,
            ]}>
            <Text style={[styles.messageText, !message.isUser && styles.aiMessageText]}>
              {message.text}
            </Text>
            <Text style={styles.timestamp}>
              {message.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
            </Text>
          </View>
        </View>
      </LongPressGestureHandler>
    </GestureHandlerRootView>
  );
}

const styles = StyleSheet.create({
  messageBubble: {
    marginBottom: 16,
    maxWidth: '80%',
    flexDirection: 'row',
    alignItems: 'flex-end',
  },
  userMessageBubble: {
    alignSelf: 'flex-end',
  },
  aiMessageBubble: {
    alignSelf: 'flex-start',
  },
  avatarContainer: {
    marginRight: 8,
  },
  avatar: {
    width: 28,
    height: 28,
    borderRadius: 14,
    backgroundColor: '#6366f1',
    justifyContent: 'center',
    alignItems: 'center',
  },
  messageContent: {
    borderRadius: 16,
    padding: 12,
    paddingBottom: 24,
    position: 'relative',
  },
  userMessageContent: {
    backgroundColor: '#6366f1',
  },
  aiMessageContent: {
    backgroundColor: '#fff',
  },
  messageText: {
    fontSize: 16,
    color: '#000',
  },
  aiMessageText: {
    color: '#222',
  },
  timestamp: {
    fontSize: 10,
    color: '#222',
    position: 'absolute',
    right: 12,
    bottom: 6,
  },
});
