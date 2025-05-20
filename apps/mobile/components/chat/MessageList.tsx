import { FlashList } from '@shopify/flash-list';
import { RefObject } from 'react';

import MessageBubble, { Message } from '~/components/chat/MessageBubble';

interface MessageListProps {
  messages: Message[];
  flatListRef: RefObject<FlashList<Message> | null>;
}

export default function MessageList({ messages, flatListRef }: MessageListProps) {
  return (
    <FlashList
      ref={flatListRef}
      data={messages}
      renderItem={({ item }) => <MessageBubble message={item} />}
      estimatedItemSize={50}
      contentContainerStyle={{ padding: 16, paddingBottom: 0 }}
      onContentSizeChange={() => flatListRef.current?.scrollToEnd({ animated: true })}
      showsVerticalScrollIndicator={false}
    />
  );
}
