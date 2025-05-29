import { FlashList } from '@shopify/flash-list';
import { useLocalSearchParams } from 'expo-router';
import { useRef } from 'react';
import { View } from 'react-native';

import ChatInput from '~/components/chat/ChatInput';
import ContactHeader from '~/components/chat/ContactHeader';
import MessageList from '~/components/chat/MessageList';
import TypingIndicator from '~/components/chat/TypingIndicator';
import Empty from '~/components/shared/Empty';
import KeyboardAvoid from '~/components/shared/KeyboardAvoid';
import Loading from '~/components/shared/Loading';
import { useChat } from '~/hooks/useChat';
import { Message } from '~/types/chat';

export default function ContactDetails() {
  const { id } = useLocalSearchParams<{ id?: string }>();
  const flatListRef = useRef<FlashList<Message> | null>(null);

  const {
    contact,
    loading,
    messages,
    inputMessage,
    setInputMessage,
    sendingMessage,
    typingIndicator,
    handleSendMessage,
  } = useChat(id as string);

  if (!contact) {
    return <Empty />;
  }

  return (
    <View className="flex-1 bg-background">
      <ContactHeader contact={contact} />

      <KeyboardAvoid className="flex-1">
        {/* Chat area that takes all available space */}
        <View className="flex-1">
          {loading ? (
            <Loading loading={loading} />
          ) : (
            <MessageList messages={messages} flatListRef={flatListRef} contactId={id as string} />
          )}
        </View>

        {/* Bottom area with typing indicator and input */}
        <View className="bg-background">
          <TypingIndicator typingIndicator={typingIndicator} />
          <ChatInput
            inputMessage={inputMessage}
            setInputMessage={setInputMessage}
            handleSendMessage={handleSendMessage}
            sendingMessage={sendingMessage}
          />
        </View>
      </KeyboardAvoid>
    </View>
  );
}
