import { useEffect, useState } from 'react';

import { getInitialGreeting, sendChatMessage } from '~/services/chatService';
import { getContactById } from '~/services/contactService';
import { Message } from '~/types/chat';
import { Contact } from '~/types/contact';

export function useChat(contactId: string) {
  const [contact, setContact] = useState<Contact | null>(null);
  const [loading, setLoading] = useState(true);
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputMessage, setInputMessage] = useState('');
  const [sendingMessage, setSendingMessage] = useState(false);
  const [typingIndicator, setTypingIndicator] = useState<{
    id: string;
    isTyping: boolean;
  } | null>(null);

  // Initialize chat
  useEffect(() => {
    if (!contactId) return;

    // Load contact and greeting
    const initializeChat = async () => {
      try {
        // Get contact data
        const contactData = await getContactById(contactId);
        console.log(`Contact with id ${contactId} fetched:`, JSON.stringify(contactData));
        setContact(contactData);

        // Get initial greeting
        const greetingData = await getInitialGreeting(contactId);

        // Add greeting as first message
        setMessages([
          {
            id: '0',
            text: greetingData.greeting,
            isUser: false,
            timestamp: new Date(),
          },
        ]);
      } catch (error) {
        console.error('Error initializing chat:', error);
        // Fallback greeting if needed and contact is available
        if (contact) {
          setMessages([
            {
              id: '0',
              text: `Hello! I'm your AI assistant for building a rich profile for ${contact.name}. I can help suggest conversation topics, activities to do together, or ways to strengthen your relationship. What would you like to know about or add to their profile?`,
              isUser: false,
              timestamp: new Date(),
            },
          ]);
        }
      } finally {
        setLoading(false);
      }
    };

    initializeChat();
  }, [contactId]);

  // Send message handler
  const handleSendMessage = async () => {
    if (inputMessage.trim().length === 0 || !contact) return;

    // Create and add user message with explicit Date object
    const userMsg = {
      id: Date.now().toString(),
      text: inputMessage,
      isUser: true,
      timestamp: new Date(),
    };
    setMessages((prev) => [...prev, userMsg]);
    setInputMessage('');
    setSendingMessage(true);

    // Show typing indicator
    setTypingIndicator({
      id: Date.now().toString(),
      isTyping: true,
    });

    try {
      // Get AI response
      const response = await sendChatMessage(contactId, inputMessage);

      // Hide typing indicator
      setTypingIndicator(null);

      // If profile was updated, refresh contact data
      if (response.profile_suggestions && Object.keys(response.profile_suggestions).length > 0) {
        console.log('Got profile suggestions:', response.profile_suggestions);
        const updatedContact = await getContactById(contactId);
        setContact(updatedContact);
      }

      // Add AI response with explicit Date object
      const aiMsg = {
        id: Date.now().toString(),
        text: response.bot_response,
        isUser: false,
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, aiMsg]);
    } catch (error) {
      console.error('Error getting AI response:', error);
      setTypingIndicator(null);
    } finally {
      setSendingMessage(false);
    }
  };

  return {
    contact,
    loading,
    messages,
    inputMessage,
    setInputMessage,
    sendingMessage,
    typingIndicator,
    handleSendMessage,
  };
}
