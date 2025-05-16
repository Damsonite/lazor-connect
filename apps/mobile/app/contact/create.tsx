import { router } from 'expo-router';
import React, { useState } from 'react';
import { ActivityIndicator, Alert, Button, StyleSheet, Text, TextInput, View } from 'react-native';

import { createContact } from '../../services/api';

const ContactCreate: React.FC = () => {
  const [firstName, setFirstName] = useState('');
  const [lastName, setLastName] = useState('');
  const [phone, setPhone] = useState('');
  const [email, setEmail] = useState('');
  const [company, setCompany] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async () => {
    if (!firstName || !lastName) {
      Alert.alert('Error', 'First and last name are required');
      return;
    }

    setIsLoading(true);
    setError(null);

    try {
      await createContact({
        first_name: firstName,
        last_name: lastName,
        email: email || undefined,
        phone_numbers: phone ? [phone] : [],
        company: company || undefined,
        tags: [],
      });

      Alert.alert('Success', 'Contact created successfully');

      // Reset form
      setFirstName('');
      setLastName('');
      setPhone('');
      setEmail('');
      setCompany('');

      // Navigate back to contact list
      router.back();
    } catch (err) {
      console.error('Failed to create contact:', err);
      setError('Failed to create contact. Please try again.');
      Alert.alert('Error', 'Failed to create contact. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Create New Contact</Text>

      {error && <Text style={styles.error}>{error}</Text>}

      <Text style={styles.label}>First Name *</Text>
      <TextInput
        style={styles.input}
        placeholder="Enter first name"
        value={firstName}
        onChangeText={setFirstName}
      />

      <Text style={styles.label}>Last Name *</Text>
      <TextInput
        style={styles.input}
        placeholder="Enter last name"
        value={lastName}
        onChangeText={setLastName}
      />

      <Text style={styles.label}>Phone</Text>
      <TextInput
        style={styles.input}
        placeholder="Enter phone number"
        value={phone}
        onChangeText={setPhone}
        keyboardType="phone-pad"
      />

      <Text style={styles.label}>Email</Text>
      <TextInput
        style={styles.input}
        placeholder="Enter email"
        value={email}
        onChangeText={setEmail}
        keyboardType="email-address"
        autoCapitalize="none"
      />

      <Text style={styles.label}>Company</Text>
      <TextInput
        style={styles.input}
        placeholder="Enter company"
        value={company}
        onChangeText={setCompany}
      />

      {isLoading ? (
        <ActivityIndicator size="large" color="#0000ff" style={styles.loader} />
      ) : (
        <Button title="Create Contact" onPress={handleSubmit} />
      )}
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 24,
    backgroundColor: '#fff',
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    marginBottom: 20,
  },
  label: {
    marginTop: 12,
    marginBottom: 4,
    fontSize: 16,
    fontWeight: '500',
  },
  input: {
    borderWidth: 1,
    borderColor: '#ccc',
    borderRadius: 6,
    padding: 10,
    fontSize: 16,
    marginBottom: 8,
  },
  error: {
    color: 'red',
    marginBottom: 10,
  },
  loader: {
    marginTop: 20,
  },
});

export default ContactCreate;
