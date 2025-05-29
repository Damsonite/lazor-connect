import { useColorScheme } from 'nativewind';
import { ReactNode } from 'react';
import { Text, View, ViewProps } from 'react-native';

import { withOpacity } from '~/utils/colors';
import { formatDate } from '~/utils/date';

type ContactDetailFieldProps = {
  label: string;
  inline?: boolean;
  value?: string | string[] | Date | number | null;
  formatter?: (val: any) => string;
  children?: ReactNode;
} & ViewProps;

export default function ContactDetailField({
  label,
  inline = true,
  value,
  formatter,
  children,
  ...props
}: ContactDetailFieldProps) {
  const { colorScheme } = useColorScheme();
  const mode = colorScheme ?? 'light';

  // Debug logging
  console.log(`📝 ContactDetail '${label}': ${value ? 'has value' : 'no value'}`);

  const renderValue = () => {
    let text = '';

    if (value === null || value === undefined) return null;
    if (Array.isArray(value) && value.length === 0) return null;

    if (Array.isArray(value)) {
      text = value.join(', ');
    } else if (formatter) {
      text = formatter(value);
    } else if (value instanceof Date) {
      text = formatDate(value);
    } else if (typeof value === 'string') {
      if (/^\d{4}-\d{2}-\d{2}T?/.test(value) || /^\d{4}-\d{2}-\d{2}$/.test(value)) {
        const formattedDate = formatDate(value);
        text = formattedDate || value;
      } else {
        text = value;
      }
    } else if (typeof value === 'number') {
      text = value.toString();
    } else {
      return null;
    }

    if (!text.trim()) return null;

    return <Text className="text-md font-itregular text-text">{text}</Text>;
  };

  const renderedValue = renderValue();

  if (!renderedValue && !children) {
    return null;
  }

  return (
    <View className={`mb-1 ${inline ? 'flex-row' : 'flex-col'}`} {...props}>
      <Text
        className={`${inline ? 'mr-1' : ''} font-itmedium`}
        style={{ color: withOpacity('text', 0.5, mode) }}>
        {label}:
      </Text>
      {renderedValue || children}
    </View>
  );
}
