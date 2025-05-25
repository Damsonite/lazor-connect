import { SafeAreaView } from 'react-native';

export default function Container({ children }: { children: React.ReactNode }) {
  return <SafeAreaView className="bg-background flex flex-1 p-4">{children}</SafeAreaView>;
}
