import { router } from 'expo-router';
import { Formik } from 'formik';
import { Tag, User } from 'lucide-react-native';
import React, { useState } from 'react';
import { ScrollView } from 'react-native';
import * as Yup from 'yup';

import SaveBtn from '~/components/contacts/SaveBtn';
import Container from '~/components/shared/Container';
import FormField from '~/components/shared/FormField';
import Loading from '~/components/shared/Loading';
import { createContact } from '~/services/contactService';

const ContactSchema = Yup.object().shape({
  name: Yup.string().required('Name is required'),
  nickname: Yup.string().optional(),
});

const ContactCreate: React.FC = () => {
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (values: { name: string; nickname: string }) => {
    setIsLoading(true);
    setError(null);

    try {
      const contactData = {
        name: values.name,
        ...(values.nickname ? { nickname: values.nickname } : {}),
      };

      await createContact(contactData);
      router.back();
    } catch (err) {
      console.error('Failed to create contact:', err);
      setError('Failed to create contact. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Container>
      <Formik
        initialValues={{ name: '', nickname: '' }}
        validationSchema={ContactSchema}
        onSubmit={handleSubmit}>
        {({
          handleChange,
          handleSubmit,
          values,
          errors,
          touched,
          setFieldTouched,
          isValid,
          dirty,
        }) => (
          <>
            <ScrollView>
              <FormField
                label="Name"
                icon={User}
                value={values.name}
                onChangeText={handleChange('name')}
                onBlur={() => setFieldTouched('name')}
                error={touched.name ? errors.name : undefined}
              />

              <FormField
                label="Nickname"
                icon={Tag}
                value={values.nickname}
                onChangeText={handleChange('nickname')}
                onBlur={() => setFieldTouched('nickname')}
              />

              <Loading loading={isLoading} error={error} />
            </ScrollView>

            <SaveBtn onPress={handleSubmit} disabled={isLoading || !isValid || !dirty} />
          </>
        )}
      </Formik>
    </Container>
  );
};

export default ContactCreate;
