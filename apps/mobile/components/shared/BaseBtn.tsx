import { forwardRef } from 'react';
import { Text, TouchableOpacity, TouchableOpacityProps, View } from 'react-native';

type ButtonProps = {
  title?: string;
  children?: React.ReactNode;
} & TouchableOpacityProps;

const Button = forwardRef<View, ButtonProps>(({ title, children, ...touchableProps }, ref) => {
  return (
    <TouchableOpacity
      ref={ref}
      {...touchableProps}
      className={`bg-primary items-center justify-center rounded-[28px] p-4 shadow-md ${touchableProps.className}`}>
      {title && <Text className="text-center text-lg font-semibold text-white">{title}</Text>}
      {children && children}
    </TouchableOpacity>
  );
});

export default Button;
