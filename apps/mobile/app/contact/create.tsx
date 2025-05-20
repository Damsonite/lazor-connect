import { router } from 'expo-router';
import React, { useState } from 'react';

import SaveBtn from '~/components/contacts/SaveBtn';
import Container from '~/components/shared/Container';
import FormField from '~/components/shared/FormField';
import Loading from '~/components/shared/Loading';
import { createContact } from '~/services/contactService';

const ContactCreate: React.FC = () => {
  const [name, setName] = useState('');
  const [isNameValid, setIsNameValid] = useState(true);
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
      await createContact({ name });

      // Reset form and validation state
      setName('');
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
      <FormField
        label="Name"
        required
        value={name}
        onChangeText={setName}
        placeholder="Enter name"
        onValidationChange={setIsNameValid}
        validateOnSubmit={shouldValidate}
      />

      <Loading loading={isLoading} error={error} />

      {!isLoading && <SaveBtn onPress={handleSubmit} />}
    </Container>
  );
};

export default ContactCreate;
