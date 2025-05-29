import { Image } from 'expo-image';
import { useSegments } from 'expo-router';
import { useColorScheme } from 'nativewind';
import { useEffect, useState } from 'react';
import { Dimensions, Text, View } from 'react-native';

import ContactSidebar from '~/components/layout/ContactSidebar';
import { useSelectedContact } from '~/context/SelectedContactProvider';
import { withOpacity } from '~/utils/colors';

interface DesktopLayoutProps {
  children: React.ReactNode;
}

export default function DesktopLayout({ children }: DesktopLayoutProps) {
  const segments = useSegments();
  const { setSelectedContactId } = useSelectedContact();
  const [dimensions, setDimensions] = useState(Dimensions.get('window'));
  const { colorScheme } = useColorScheme();
  const mode = colorScheme ?? 'light';

  useEffect(() => {
    const subscription = Dimensions.addEventListener('change', ({ window }) => {
      setDimensions(window);
    });

    return () => subscription?.remove();
  }, []);

  useEffect(() => {
    if (segments.length >= 2 && segments[0] === 'contact' && segments[1] !== 'create') {
      setSelectedContactId(segments[1] as string);
    } else {
      setSelectedContactId(null);
    }
  }, [segments, setSelectedContactId]);

  const isContactDetail =
    segments.length >= 2 && segments[0] === 'contact' && segments[1] !== 'create';

  const isMainPage = segments[0] !== 'contact';

  if (!(dimensions.width >= 768)) {
    return <>{children}</>;
  }

  return (
    <View className="flex-1 flex-row bg-background">
      <View className="w-1/3 max-w-xs border-r border-gray">
        <ContactSidebar />
      </View>

      <View className="flex-1">
        {isContactDetail ? (
          children
        ) : isMainPage ? (
          <View className="flex-1 items-center justify-center">
            <View className="max-w-md justify-center">
              <View className="h-40 w-40">
                <Image
                  className="h-full w-full"
                  source={require('~/assets/adaptive-icon.png')}
                  contentFit="cover"
                />
              </View>

              <View className="ml-8">
                <Text className="mb-2 font-orbitron text-2xl text-primary">
                  LazorConnect Desktop
                </Text>

                <Text
                  className="font-itregular text-base leading-relaxed text-gray"
                  style={{ color: withOpacity('text', 0.5, mode) }}>
                  Select a contact from the sidebar to start a conversation, or create a new contact
                  to begin building your network.
                </Text>
              </View>
            </View>
          </View>
        ) : (
          children
        )}
      </View>
    </View>
  );
}
