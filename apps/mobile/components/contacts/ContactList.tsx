import { useEffect, useState } from 'react';
import { ActivityIndicator, Text, View } from 'react-native';

import AddBtn from './AddBtn';
import ContactItem from './ContactItem';

import List from '~/components/shared/List';
import { getContacts } from '~/services/contactService';
import { Contact } from '~/types/contact';

export default function ContactList() {
  const [contacts, setContacts] = useState<Contact[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchContacts = async () => {
      try {
        const data = await getContacts();
        setContacts(data);
        setLoading(false);
      } catch (err) {
        console.error('Error fetching contacts:', err);
        setError('Failed to load contacts. Please try again later.');
        setLoading(false);
      }
    };

    fetchContacts();
  }, []);

  if (loading) {
    return (
      <View className="flex-1 items-center justify-center">
        <ActivityIndicator size="large" color="#0000ff" />
      </View>
    );
  }

  if (error) {
    return (
      <View className="flex-1 items-center justify-center p-4">
        <Text className="text-center text-red-500">{error}</Text>
      </View>
    );
  }

  return (
    <View className="flex-1">
      <List data={contacts} renderItem={({ item }) => <ContactItem contact={item} />} />
      <AddBtn />
    </View>
  );
}
