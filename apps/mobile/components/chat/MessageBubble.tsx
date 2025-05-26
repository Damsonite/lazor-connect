import { Bot } from 'lucide-react-native';
import { useColorScheme } from 'nativewind';
import { Alert, Text, View } from 'react-native';
import {
  GestureHandlerRootView,
  LongPressGestureHandler,
  State,
} from 'react-native-gesture-handler';

import { submitFeedback } from '~/services/feedbackService';
import { Message } from '~/types/chat';
import { colors, withOpacity } from '~/utils/colors';
import { formatChatTimestamp } from '~/utils/date';

export interface MessageBubbleProps {
  message: Message;
  contactId: string;
}

export default function MessageBubble({ message, contactId }: MessageBubbleProps) {
  const { colorScheme } = useColorScheme();
  const mode = colorScheme ?? 'light';

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
          className={`mb-4 max-w-[80%] flex-row items-end ${message.isUser ? 'self-end' : 'self-start'}`}>
          {!message.isUser && (
            <View className="mr-2">
              <Bot size={24} color={colors.primary[mode]} />
            </View>
          )}
          <View
            style={{
              backgroundColor: message.isUser ? withOpacity('primary', 0.4, mode) : 'white',
            }}
            className="relative rounded-2xl border border-gray-200 p-4 pb-6">
            <Text className="font-itregular text-lg text-text">{message.text}</Text>
            <Text
              className="absolute bottom-2 right-3 font-itregular text-sm"
              style={{ color: withOpacity('text', 0.5, mode) }}>
              {formatChatTimestamp(message.timestamp)}
            </Text>
          </View>
        </View>
      </LongPressGestureHandler>
    </GestureHandlerRootView>
  );
}
