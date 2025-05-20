import { ReactNode } from 'react';
import { Text, View, ViewProps } from 'react-native';

type ContactDetailFieldProps = {
  label: string;
  inline?: boolean;
  children: ReactNode;
} & ViewProps;

export default function ContactDetailField({
  label,
  inline = true,
  children,
  ...props
}: ContactDetailFieldProps) {
  return (
    <View className={`mb-1 ${inline ? 'flex-row' : 'flex-col'}`} {...props}>
      <Text className={`${inline ? 'mr-1' : ''} text-gray-500`}>{label}:</Text>
      {typeof children === 'string' ? (
        <Text className="text-md text-slate-800">{children}</Text>
      ) : (
        children
      )}
    </View>
  );
}
