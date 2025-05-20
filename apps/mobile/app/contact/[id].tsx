import { useLocalSearchParams } from 'expo-router';
import React from 'react';
import { ActivityIndicator, StyleSheet, Text, View } from 'react-native';

// Mock function to fetch contact details
const fetchContactById = async (id: string) => {
  // Replace with real API call
  return new Promise<{ id: string; name: string; email: string; phone: string }>((resolve) =>
    setTimeout(
      () =>
        resolve({
          id,
          name: 'John Doe',
          email: 'john.doe@example.com',
          phone: '+1 234 567 890',
        }),
      500
    )
  );
};

const ContactDetailsPage = () => {
  const { id } = useLocalSearchParams<{ id?: string }>();
  const [contact, setContact] = React.useState<null | {
    id: string;
    name: string;
    email: string;
    phone: string;
  }>(null);
  const [loading, setLoading] = React.useState(true);

  React.useEffect(() => {
    if (id) {
      fetchContactById(id).then((data) => {
        setContact(data);
        setLoading(false);
      });
    }
  }, [id]);

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
    <View style={styles.container}>
      <Text style={styles.title}>{contact.name}</Text>
      <Text style={styles.label}>Email:</Text>
      <Text style={styles.value}>{contact.email}</Text>
      <Text style={styles.label}>Phone:</Text>
      <Text style={styles.value}>{contact.phone}</Text>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 24,
    backgroundColor: '#fff',
  },
  centered: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  title: {
    fontSize: 28,
    fontWeight: 'bold',
    marginBottom: 24,
  },
  label: {
    fontSize: 16,
    color: '#888',
    marginTop: 12,
  },
  value: {
    fontSize: 18,
    color: '#222',
    marginTop: 4,
  },
});

export default ContactDetailsPage;
