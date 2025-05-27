import { View } from 'react-native';

export default function Container({ children }: { children: React.ReactNode }) {
  return <View className="flex flex-1 bg-background p-4 pb-0">{children}</View>;
}
