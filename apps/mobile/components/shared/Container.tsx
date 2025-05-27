import { Image, View } from 'react-native';

export default function Container({ children }: { children: React.ReactNode }) {
  return (
    <View className="flex-1">
      <Image
        source={require('~/assets/splash.png')}
        className="absolute h-full w-full opacity-5"
        resizeMode="center"
        style={{ transform: [{ scale: 1.5 }] }}
      />

      <View className="flex flex-1 p-4 pb-0">{children}</View>
    </View>
  );
}
