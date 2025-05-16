import { FlashList, ListRenderItem } from '@shopify/flash-list';
import { Text, View } from 'react-native';

interface ListProps<T> {
  data: T[];
  renderItem: ListRenderItem<T>;
}

export default function List<T>({ data, renderItem }: ListProps<T>) {
  return (
    <View className="flex-1">
      <FlashList
        data={data}
        renderItem={renderItem}
        estimatedItemSize={80}
        ListEmptyComponent={() => (
          <View className="flex-1 items-center justify-center p-4">
            <Text className="text-center text-gray-500">
              No contacts found. Add your first contact!
            </Text>
          </View>
        )}
      />
    </View>
  );
}
