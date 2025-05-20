import React, { useEffect, useState } from 'react';
import { Text, TextInput, View } from 'react-native';

interface FormFieldProps {
  label: string;
  value: string;
  onChangeText: (text: string) => void;
  placeholder?: string;
  required?: boolean;
  multiline?: boolean;
  numberOfLines?: number;
  keyboardType?: 'default' | 'email-address' | 'numeric' | 'phone-pad' | 'url';
  onBlur?: () => void;
  onValidationChange?: (isValid: boolean) => void;
  validateOnSubmit?: boolean;
}

const FormField: React.FC<FormFieldProps> = ({
  label,
  value,
  onChangeText,
  placeholder,
  required = false,
  multiline = false,
  numberOfLines = 1,
  keyboardType = 'default',
  onBlur,
  onValidationChange,
  validateOnSubmit = false,
}) => {
  const [error, setError] = useState<string | null>(null);

  // Effect to handle validateOnSubmit prop change
  useEffect(() => {
    if (validateOnSubmit) {
      validate();
    }
  }, [validateOnSubmit]);

  const validate = () => {
    // Call external onBlur if provided
    if (onBlur) onBlur();

    // Only validate required fields
    if (required && !value) {
      setError(`${label} is required`);
      if (onValidationChange) onValidationChange(false);
      return false;
    }

    // Field is valid
    setError(null);
    if (onValidationChange) onValidationChange(true);
    return true;
  };

  return (
    <View className="mb-4">
      <Text className="mb-1 text-lg font-medium">
        {label} {required && <Text className="text-red-500">*</Text>}
      </Text>
      <TextInput
        className={`mb-2 rounded-md border p-3 ${error ? 'border-red-500' : 'border-gray-400'}`}
        placeholder={placeholder || `Enter ${label.toLowerCase()}`}
        value={value}
        onChangeText={(text) => {
          onChangeText(text);
          if (error && text) {
            setError(null);
            if (onValidationChange) onValidationChange(true);
          }
        }}
        onBlur={validate}
        multiline={multiline}
        numberOfLines={multiline ? numberOfLines : 1}
        keyboardType={keyboardType}
      />
      {error && <Text className="text-sm text-red-500">{error}</Text>}
    </View>
  );
};

export default FormField;
