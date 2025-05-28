import { Text, View } from 'react-native';

export default function Empty({ message }: { message?: string }) {
  return (
    <View className="flex-1 items-center justify-center p-4">
      <Text className="text-center text-text">{message}</Text>
    </View>
  );
}
