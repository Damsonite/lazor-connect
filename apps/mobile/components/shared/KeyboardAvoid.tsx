import React, { useEffect, useState } from 'react';
import { Animated, Dimensions, Keyboard, KeyboardEvent, Platform, ViewProps } from 'react-native';

interface KeyboardAvoidProps extends ViewProps {
  children: React.ReactNode;
}

const KeyboardAvoid: React.FC<KeyboardAvoidProps> = ({ children, style, ...props }) => {
  const [keyboardHeight] = useState(new Animated.Value(0));
  const [dimensions, setDimensions] = useState(Dimensions.get('window'));

  useEffect(() => {
    const subscription = Dimensions.addEventListener('change', ({ window }) => {
      setDimensions(window);
    });

    return () => subscription?.remove();
  }, []);

  useEffect(() => {
    // Don't apply keyboard avoidance on desktop (screens ≥768px)
    const isDesktop = dimensions.width >= 768;
    if (isDesktop) {
      return;
    }

    const keyboardShowEventName = Platform.OS === 'ios' ? 'keyboardWillShow' : 'keyboardDidShow';
    const keyboardHideEventName = Platform.OS === 'ios' ? 'keyboardWillHide' : 'keyboardDidHide';

    const keyboardShowListener = Keyboard.addListener(
      keyboardShowEventName,
      (event: KeyboardEvent) => {
        const height = event.endCoordinates.height;
        Animated.timing(keyboardHeight, {
          toValue: height,
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
  }, [keyboardHeight, dimensions.width]);

  const isDesktop = dimensions.width >= 768;

  return (
    <Animated.View
      style={[{ flex: 1 }, isDesktop ? {} : { paddingBottom: keyboardHeight }, style]}
      {...props}>
      {children}
    </Animated.View>
  );
};

export default KeyboardAvoid;
