import { LucideIcon } from 'lucide-react-native';
import { useColorScheme } from 'nativewind';
import React, { useState } from 'react';
import { Text, TextInput, View } from 'react-native';

import { colors, withOpacity } from '~/utils/colors';

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
  const { colorScheme } = useColorScheme();
  const mode = colorScheme ?? 'light';

  const getBorderColor = () => {
    if (error) return colors.danger[mode];
    if (isFocused) return colors.primary[mode];
    return withOpacity('text', 0.5, mode);
  };

  return (
    <View className="mb-4 flex-row">
      {icon && (
        <View className="size-14 items-center justify-center">
          {icon && React.createElement(icon, { color: colors.text[mode] })}
        </View>
      )}

      <View className="flex-1">
        <TextInput
          style={{ borderColor: getBorderColor(), color: colors.text[mode] }}
          className="mb-2 w-full rounded-lg border-2 px-3 py-3 font-itmedium tracking-wider"
          placeholder={label}
          placeholderTextColor={withOpacity('text', 0.5, mode)}
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
