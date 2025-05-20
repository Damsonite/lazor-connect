import '~/global.css';

import { Stack } from 'expo-router';
import { StatusBar } from 'react-native';

export default function Layout() {
  return (
    <>
      <Stack>
        <Stack.Screen name="index" options={{ title: 'Lazor Connect' }} />
        <Stack.Screen name="contact/create" options={{ title: 'Create contact' }} />
        <Stack.Screen name="contact/[id]" options={{ title: 'Chat Assistant' }} />
      </Stack>

      <StatusBar />
    </>
  );
}
