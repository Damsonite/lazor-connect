import { SafeAreaView } from 'react-native';

export default function Container({ children }: { children: React.ReactNode }) {
  return <SafeAreaView className="m-6 flex flex-1">{children}</SafeAreaView>;
}
