import { useColorScheme } from 'nativewind';
import { ActivityIndicator, Text, View } from 'react-native';

import { colors } from '~/utils/colors';

interface LoadingIndicatorProps {
  loading: boolean;
  error?: string | undefined;
}

export default function Loading({ loading, error }: LoadingIndicatorProps) {
  const { colorScheme } = useColorScheme();
  const mode = colorScheme ?? 'light';

  if (loading) {
    return (
      <View className="items-center justify-center py-8">
        <ActivityIndicator size="large" color={colors.primary[mode]} />
      </View>
    );
  }

  if (error) {
    return (
      <View className="items-center justify-center p-4">
        <Text className="text-center text-red-500">{error}</Text>
      </View>
    );
  }

  return null;
}
