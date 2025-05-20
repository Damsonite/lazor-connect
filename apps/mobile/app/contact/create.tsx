import { router } from 'expo-router';
import React, { useState } from 'react';
import { ScrollView } from 'react-native';

import SaveBtn from '~/components/contacts/SaveBtn';
import Container from '~/components/shared/Container';
import FormField from '~/components/shared/FormField';
import Loading from '~/components/shared/Loading';
import { createContact } from '~/services/contactService';

const ContactCreate: React.FC = () => {
  const [name, setName] = useState('');
  const [isNameValid, setIsNameValid] = useState(true);
  const [personality, setPersonality] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [shouldValidate, setShouldValidate] = useState(false);

  const handleSubmit = async () => {
    setShouldValidate(true);

    // Check if required field is filled
    if (!name || !isNameValid) {
      return;
    }

    setIsLoading(true);
    setError(null);

    try {
      // Include personality if provided
      await createContact({
        name,
        ...(personality ? { personality } : {}),
      });

      // Reset form and validation state
      setName('');
      setPersonality('');
      setShouldValidate(false);

      // Navigate back to contact list
      router.back();
    } catch (err) {
      console.error('Failed to create contact:', err);
      setError('Failed to create contact. Please try again.');
      setShouldValidate(false);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Container>
      <ScrollView style={{ flex: 1, width: '100%' }}>
        <FormField
          label="Name"
          required
          value={name}
          onChangeText={setName}
          placeholder="Enter name"
          onValidationChange={setIsNameValid}
          validateOnSubmit={shouldValidate}
        />

        <FormField
          label="Personality"
          value={personality}
          onChangeText={setPersonality}
          placeholder="Describe personality traits, emotional characteristics, and behaviors"
          multiline
          numberOfLines={5}
        />

        <Loading loading={isLoading} error={error} />
      </ScrollView>

      {!isLoading && <SaveBtn onPress={handleSubmit} />}
    </Container>
  );
};

export default ContactCreate;
