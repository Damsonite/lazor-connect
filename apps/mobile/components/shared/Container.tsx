import { View } from 'react-native';

export default function Container({ children }: { children: React.ReactNode }) {
  return <View className="bg-background flex flex-1 p-4">{children}</View>;
}
