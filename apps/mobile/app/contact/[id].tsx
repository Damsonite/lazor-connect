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
import { Message } from '~/components/chat/MessageBubble';
import MessageList from '~/components/chat/MessageList';
import TypingIndicator from '~/components/chat/TypingIndicator';
import { getContactById } from '~/services/contactService';
import { Contact } from '~/types/contact';

// Mock function to simulate AI responses
const getAIResponse = async (message: string, contactName: string): Promise<string> => {
  // This would be replaced with a real AI API call (e.g., Gemini)
  return new Promise((resolve) => {
    setTimeout(() => {
      const responses = [
        `I've noted that about ${contactName}. Is there anything else you'd like me to remember?`,
        `That's interesting! Would you like me to update ${contactName}'s profile with this information?`,
        `Thanks for sharing. Based on ${contactName}'s interests, you might want to discuss recent photography exhibitions next time you meet.`,
        `I'll remember that for future conversations about ${contactName}.`,
      ];
      const randomResponse = responses[Math.floor(Math.random() * responses.length)];
      resolve(randomResponse);
    }, 1000);
  });
};

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

      getContactById(contactId)
        .then((data) => {
          setContact(data);
          setLoading(false);

          // Add initial AI message
          const welcomeMessage: Message = {
            id: '0',
            text: `Hey there! I'm your AI assistant for managing your relationship with ${data.name}. You can ask me about their interests, update their information, or set reminders for reaching out.`,
            isUser: false,
            timestamp: new Date(),
          };
          setMessages([welcomeMessage]);
        })
        .catch((error) => {
          console.error('Error fetching contact:', error);
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
      const response = await getAIResponse(inputMessage, contact.name);

      // Hide typing indicator
      setTypingIndicator(null);

      // Add AI response to the list
      const aiMessage: Message = {
        id: Date.now().toString(),
        text: response,
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
