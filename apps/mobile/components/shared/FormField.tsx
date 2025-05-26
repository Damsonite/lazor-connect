import { LucideIcon } from 'lucide-react-native';
import React, { useState } from 'react';
import { Text, TextInput, View } from 'react-native';

interface FormFieldProps {
  label: string;
  icon?: LucideIcon;
  value: string;
  onChangeText: (text: string) => void;
  onBlur?: () => void;
  error?: string;
  multiline?: boolean;
  numberOfLines?: number;
  keyboardType?: 'default' | 'email-address' | 'numeric' | 'phone-pad' | 'url';
}

const FormField: React.FC<FormFieldProps> = ({
  label,
  icon,
  value,
  onChangeText,
  onBlur,
  error,
  multiline = false,
  numberOfLines = 1,
  keyboardType = 'default',
}) => {
  const [isFocused, setIsFocused] = useState(false);

  const getBorderClass = () => {
    if (error) return 'border-danger';
    if (isFocused) return 'border-primary';
    return 'border-gray-400';
  };

  return (
    <View className="mb-4 flex-row">
      {icon && (
        <View className="size-14 items-center justify-center">{React.createElement(icon)}</View>
      )}

      <View className="flex-1">
        <TextInput
          className={`mb-2 h-14 w-full rounded-lg border-2 px-3 font-itmedium tracking-wider ${getBorderClass()}`}
          placeholder={label}
          value={value}
          onFocus={() => setIsFocused(true)}
          onChangeText={(text) => {
            onChangeText(text);
          }}
          onBlur={() => {
            setIsFocused(false);
            if (onBlur) onBlur();
          }}
          multiline={multiline}
          numberOfLines={multiline ? numberOfLines : 1}
          keyboardType={keyboardType}
        />
        {error && <Text className="ml-1 font-itregular text-sm text-danger">{error}</Text>}
      </View>
    </View>
  );
};

export default FormField;
