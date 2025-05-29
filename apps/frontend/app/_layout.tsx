import { Exo2_500Medium, Exo2_600SemiBold } from '@expo-google-fonts/exo-2';
import { Inter_400Regular, Inter_500Medium } from '@expo-google-fonts/inter';
import { Orbitron_700Bold } from '@expo-google-fonts/orbitron';
import { useFonts } from 'expo-font';
import { Stack } from 'expo-router';
import * as SplashScreen from 'expo-splash-screen';
import { useColorScheme } from 'nativewind';
import { useEffect, useState } from 'react';
import { Dimensions } from 'react-native';

import DesktopLayout from '~/components/layout/DesktopLayout';
import { SelectedContactProvider } from '~/context/SelectedContactProvider';
import ThemeProvider from '~/context/ThemeProvider';
import '~/global.css';
import { colors } from '~/utils/colors';

SplashScreen.preventAutoHideAsync();

export default function RootLayout() {
  const { colorScheme } = useColorScheme();
  const mode = colorScheme ?? 'light';
  const [dimensions, setDimensions] = useState(Dimensions.get('window'));

  const [loaded, error] = useFonts({
    Orbitron: Orbitron_700Bold,
    InterRegular: Inter_400Regular,
    InterMedium: Inter_500Medium,
    ExoMedium: Exo2_500Medium,
    ExoSemiBold: Exo2_600SemiBold,
  });

  useEffect(() => {
    if (loaded || error) {
      SplashScreen.hideAsync();
    }
  }, [loaded, error]);

  useEffect(() => {
    const subscription = Dimensions.addEventListener('change', ({ window }) => {
      setDimensions(window);
    });

    return () => subscription?.remove();
  }, []);

  const isDesktop = dimensions.width >= 768;

  if (!loaded && !error) {
    return null;
  }

  return (
    <ThemeProvider>
      <SelectedContactProvider>
        <DesktopLayout>
          <Stack
            screenOptions={{
              headerTitleStyle: {
                fontFamily: 'ExoSemiBold',
              },
              headerTintColor: colors.text[mode],
              headerStyle: {
                backgroundColor: colors.background[mode],
              },
              contentStyle: {
                backgroundColor: colors.background[mode],
              },
              presentation: 'transparentModal',
              headerShown: !isDesktop,
            }}>
            <Stack.Screen
              name="index"
              options={{
                title: 'LazorConnect',
                headerTitleStyle: {
                  fontFamily: 'Orbitron',
                  color: colors.primary[mode],
                },
                headerShadowVisible: false,
              }}
            />
            <Stack.Screen
              name="contact/create"
              options={{
                title: 'New contact',
              }}
            />
            <Stack.Screen
              name="contact/[id]"
              options={({ route }) => {
                const { name } = route.params as { name: string };
                return {
                  title: `${name}`,
                };
              }}
            />
          </Stack>
        </DesktopLayout>
      </SelectedContactProvider>
    </ThemeProvider>
  );
}
