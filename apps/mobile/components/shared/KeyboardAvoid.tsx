import React, { useEffect, useState } from 'react';
import { Animated, Keyboard, KeyboardEvent, Platform, ViewProps } from 'react-native';

interface KeyboardAvoidProps extends ViewProps {
  children: React.ReactNode;
}

const KeyboardAvoid: React.FC<KeyboardAvoidProps> = ({ children, ...props }) => {
  const [keyboardHeight] = useState(new Animated.Value(0));

  useEffect(() => {
    const keyboardShowEventName = Platform.OS === 'ios' ? 'keyboardWillShow' : 'keyboardDidShow';
    const keyboardHideEventName = Platform.OS === 'ios' ? 'keyboardWillHide' : 'keyboardDidHide';

    const keyboardShowListener = Keyboard.addListener(
      keyboardShowEventName,
      (event: KeyboardEvent) => {
        const height = event.endCoordinates.height;
        Animated.timing(keyboardHeight, {
          toValue: height - (Platform.OS === 'ios' ? 0 : 0),
          duration: 250,
          useNativeDriver: false,
        }).start();
      }
    );

    const keyboardHideListener = Keyboard.addListener(keyboardHideEventName, () => {
      Animated.timing(keyboardHeight, {
        toValue: 0,
        duration: 250,
        useNativeDriver: false,
      }).start();
    });

    return () => {
      keyboardShowListener.remove();
      keyboardHideListener.remove();
    };
  }, [keyboardHeight]);

  return (
    <Animated.View className="w-full flex-1" style={[{ paddingBottom: keyboardHeight }]} {...props}>
      {children}
    </Animated.View>
  );
};

export default KeyboardAvoid;
