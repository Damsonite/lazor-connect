import { Exo2_500Medium } from '@expo-google-fonts/exo-2';
import { Inter_400Regular, Inter_500Medium } from '@expo-google-fonts/inter';
import { Orbitron_700Bold } from '@expo-google-fonts/orbitron';
import { useFonts } from 'expo-font';
import { Stack } from 'expo-router';
import * as SplashScreen from 'expo-splash-screen';
import { useColorScheme } from 'nativewind';
import { useEffect } from 'react';

import ThemeProvider from '~/context/ThemeProvider';
import '~/global.css';
import { colors } from '~/utils/colors';

SplashScreen.preventAutoHideAsync();

export default function RootLayout() {
  const { colorScheme } = useColorScheme();
  const mode = colorScheme ?? 'light';

  const [loaded, error] = useFonts({
    Orbitron: Orbitron_700Bold,
    InterRegular: Inter_400Regular,
    InterMedium: Inter_500Medium,
    ExoMedium: Exo2_500Medium,
  });

  useEffect(() => {
    if (loaded || error) {
      SplashScreen.hideAsync();
    }
  }, [loaded, error]);

  if (!loaded && !error) {
    return null;
  }

  return (
    <ThemeProvider>
      <Stack>
        <Stack.Screen
          name="index"
          options={{
            headerTitle: 'LazorConnect',
            headerTitleStyle: {
              fontFamily: 'Orbitron',
              color: colors.primary[mode],
            },
            headerStyle: {
              backgroundColor: colors.background[mode],
            },
            headerShadowVisible: false,
          }}
        />
        <Stack.Screen name="contact/create" options={{ title: 'Create contact' }} />
        <Stack.Screen name="contact/[id]" options={{ title: 'Chat Assistant' }} />
      </Stack>
    </ThemeProvider>
  );
}
