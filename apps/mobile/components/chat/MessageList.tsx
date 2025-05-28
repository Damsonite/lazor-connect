import { FlashList } from '@shopify/flash-list';
import { RefObject } from 'react';

import MessageBubble from '~/components/chat/MessageBubble';
import { Message } from '~/types/chat';

interface MessageListProps {
  messages: Message[];
  flatListRef: RefObject<FlashList<Message> | null>;
  contactId: string;
}
export default function MessageList({ messages, flatListRef, contactId }: MessageListProps) {
  return (
    <FlashList
      className="flex-1"
      ref={flatListRef}
      data={messages}
      renderItem={({ item }) => <MessageBubble message={item} contactId={contactId} />}
      estimatedItemSize={50}
      contentContainerStyle={{ padding: 16 }}
      onContentSizeChange={() => {
        // Safe scroll to bottom with additional checks
        if (flatListRef.current && messages.length > 0) {
          try {
            setTimeout(() => {
              flatListRef.current?.scrollToEnd({ animated: true });
            }, 100);
          } catch (error) {
            console.log('Error scrolling to end:', error);
          }
        }
      }}
      showsVerticalScrollIndicator={false}
    />
  );
}
