import { useColorScheme } from 'nativewind';
import { forwardRef } from 'react';
import { Text, TouchableOpacity, TouchableOpacityProps, View } from 'react-native';

import { Color, colors, withOpacity } from '~/utils/colors';

type ButtonProps = {
  title?: string;
  children?: React.ReactNode;
  color?: Color;
  isAction?: boolean;
  disabled?: boolean;
} & TouchableOpacityProps;

const Button = forwardRef<View, ButtonProps>(
  (
    { title, children, color = 'primary', isAction = false, disabled = false, ...touchableProps },
    ref
  ) => {
    const { colorScheme } = useColorScheme();
    const mode = colorScheme ?? 'light';
    const actionClassname = isAction ? 'absolute bottom-12 right-4 size-20' : '';

    return (
      <TouchableOpacity
        ref={ref}
        {...touchableProps}
        className={`items-center justify-center rounded-3xl bg-primary p-4 shadow-md ${touchableProps.className} ${actionClassname}}`}
        style={{ backgroundColor: disabled ? withOpacity('text', 0.2, mode) : colors[color][mode] }}
        disabled={disabled}>
        {title && (
          <Text className="text-center text-lg font-semibold text-background">{title}</Text>
        )}
        {children && children}
      </TouchableOpacity>
    );
  }
);

export default Button;
