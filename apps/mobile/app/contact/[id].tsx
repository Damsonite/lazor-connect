import { FlashList } from '@shopify/flash-list';
import { useLocalSearchParams } from 'expo-router';
import { useRef } from 'react';
import { View } from 'react-native';

import ChatInput from '~/components/chat/ChatInput';
import ContactHeader from '~/components/chat/ContactHeader';
import MessageList from '~/components/chat/MessageList';
import TypingIndicator from '~/components/chat/TypingIndicator';
import Empty from '~/components/shared/Empty';
import Loading from '~/components/shared/Loading';
import { useChat } from '~/hooks/useChat';
import { Message } from '~/types/chat';

const ContactDetails = () => {
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
      <MessageList messages={messages} flatListRef={flatListRef} contactId={id as string} />

      <Loading loading={loading} />

      <TypingIndicator typingIndicator={typingIndicator} />
      <ChatInput
        inputMessage={inputMessage}
        setInputMessage={setInputMessage}
        handleSendMessage={handleSendMessage}
        sendingMessage={sendingMessage}
      />
    </View>
  );
};

export default ContactDetails;
