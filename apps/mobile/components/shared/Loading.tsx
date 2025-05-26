import { ActivityIndicator, Text, View } from 'react-native';

interface LoadingIndicatorProps {
  loading: boolean;
  error?: string | undefined;
}

export default function Loading({ loading, error }: LoadingIndicatorProps) {
  if (loading) {
    return (
      <View className="flex-1 items-center justify-center">
        <ActivityIndicator size="large" color="#0000ff" />
      </View>
    );
  }

  if (error) {
    return (
      <View className="flex-1 items-center justify-center p-4">
        <Text className="text-center text-red-500">{error}</Text>
      </View>
    );
  }

  return null;
}
