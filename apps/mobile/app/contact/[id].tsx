import { FlashList } from '@shopify/flash-list';
import { useLocalSearchParams } from 'expo-router';
import { useEffect, useRef, useState } from 'react';
import {
  ActivityIndicator,
  KeyboardAvoidingView,
  Platform,
  StyleSheet,
  Text,
  View,
} from 'react-native';

import ChatInput from '~/components/chat/ChatInput';
import ContactData from '~/components/chat/ContactData';
import MessageList from '~/components/chat/MessageList';
import TypingIndicator from '~/components/chat/TypingIndicator';
import { getInitialGreeting, sendChatMessage } from '~/services/chatService';
import { getContactById } from '~/services/contactService';
import { Message } from '~/types/chat';
import { Contact } from '~/types/contact';

const ContactDetails = () => {
  const { id } = useLocalSearchParams<{ id?: string }>();
  const [contact, setContact] = useState<Contact | null>(null);
  const [loading, setLoading] = useState(true);
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputMessage, setInputMessage] = useState('');
  const [sendingMessage, setSendingMessage] = useState(false);
  const [typingIndicator, setTypingIndicator] = useState<{
    id: string;
    isTyping: boolean;
  } | null>(null);
  const flatListRef = useRef<FlashList<Message> | null>(null);

  // Initialize chat with a welcome message
  useEffect(() => {
    if (id) {
      // Use the ID directly as a string for UUID
      const contactId = id as string;

      // First get the contact
      getContactById(contactId)
        .then((data) => {
          setContact(data);

          // Then get the initial greeting from the AI
          return getInitialGreeting(contactId);
        })
        .then((greetingData) => {
          // Add the AI greeting as the first message
          const welcomeMessage: Message = {
            id: '0',
            text: greetingData.greeting,
            isUser: false,
            timestamp: new Date(),
          };
          setMessages([welcomeMessage]);
          setLoading(false);
        })
        .catch((error) => {
          console.error('Error initializing chat:', error);

          // Fallback to a profile-building focused greeting if the API fails
          if (contact) {
            const fallbackMessage: Message = {
              id: '0',
              text: `Hello! I'm your AI assistant for building a rich profile for ${contact.name}. I can help suggest conversation topics, activities to do together, or ways to strengthen your relationship. What would you like to know about or add to their profile?`,
              isUser: false,
              timestamp: new Date(),
            };
            setMessages([fallbackMessage]);
          }
          setLoading(false);
        });
    }
  }, [id]);

  // Send message function
  const handleSendMessage = async () => {
    if (inputMessage.trim().length === 0 || !contact) return;

    // Add user message to the list
    const userMessage: Message = {
      id: Date.now().toString(),
      text: inputMessage,
      isUser: true,
      timestamp: new Date(),
    };

    setMessages((prevMessages) => [...prevMessages, userMessage]);
    setInputMessage('');
    setSendingMessage(true);

    // Show typing indicator
    setTypingIndicator({
      id: Date.now().toString(),
      isTyping: true,
    });

    // Simulate typing indicator by scrolling to bottom
    setTimeout(() => flatListRef.current?.scrollToEnd({ animated: true }), 100);

    try {
      // Get AI response
      const response = await sendChatMessage(id as string, inputMessage);

      // Hide typing indicator
      setTypingIndicator(null);

      // If there are profile suggestions, we could update the contact profile here
      if (response.profile_suggestions && Object.keys(response.profile_suggestions).length > 0) {
        console.log('Got profile suggestions:', response.profile_suggestions);
        // In a real app, you might:
        // 1. Ask the user if they want to update the profile with this information
        // 2. Automatically update certain fields
        // 3. Show a UI element with the suggested changes
      }

      // Add AI response to the list
      const aiMessage: Message = {
        id: Date.now().toString(),
        text: response.bot_response,
        isUser: false,
        timestamp: new Date(),
      };

      setMessages((prevMessages) => [...prevMessages, aiMessage]);

      // Scroll to the bottom to show the new message
      setTimeout(() => flatListRef.current?.scrollToEnd({ animated: true }), 100);
    } catch (error) {
      console.error('Error getting AI response:', error);
      setTypingIndicator(null);
    } finally {
      setSendingMessage(false);
    }
  };

  if (loading) {
    return (
      <View style={styles.centered}>
        <ActivityIndicator size="large" />
      </View>
    );
  }

  if (!contact) {
    return (
      <View style={styles.centered}>
        <Text>Contact not found.</Text>
      </View>
    );
  }

  return (
    <KeyboardAvoidingView
      style={styles.container}
      behavior={Platform.OS === 'ios' ? 'padding' : undefined}
      keyboardVerticalOffset={100}>
      <ContactData contact={contact} />

      <MessageList messages={messages} flatListRef={flatListRef} />

      <TypingIndicator typingIndicator={typingIndicator} />

      <ChatInput
        inputMessage={inputMessage}
        setInputMessage={setInputMessage}
        handleSendMessage={handleSendMessage}
        sendingMessage={sendingMessage}
      />
    </KeyboardAvoidingView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
  },
  centered: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
});

export default ContactDetails;
