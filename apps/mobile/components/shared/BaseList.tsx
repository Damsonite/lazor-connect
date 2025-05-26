import { FlashList, ListRenderItem } from '@shopify/flash-list';
import { useEffect, useState } from 'react';
import { Text, View } from 'react-native';

import LoadingIndicator from '~/components/shared/Loading';

interface ListProps<T> {
  fetchData: () => Promise<T[]>;
  renderItem: ListRenderItem<T>;
  emptyMessage?: string;
}

export default function BaseList<T>({
  fetchData,
  renderItem,
  emptyMessage = 'No items found',
}: ListProps<T>) {
  const [data, setData] = useState<T[]>([]);
  const [loading, setLoading] = useState<boolean>(!!fetchData);
  const [error, setError] = useState<string | null>(null);

  const loadData = async () => {
    if (!fetchData) return;

    setLoading(true);
    setError(null);

    try {
      const result = await fetchData();
      setData(result);
    } catch (err) {
      console.error('Error fetching data:', err);
      setError('Failed to load data. Please try again later.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, [fetchData]);

  const EmptyComponent = () => (
    <View className="flex-1 items-center justify-center p-4">
      <Text className="text-center text-gray-500">{emptyMessage}</Text>
    </View>
  );

  return (
    <View className="bg-backround flex-1">
      <LoadingIndicator loading={loading} error={error} />
      {!loading && !error && (
        <FlashList
          data={data}
          renderItem={renderItem}
          estimatedItemSize={80}
          onRefresh={loadData}
          refreshing={loading}
          ListEmptyComponent={EmptyComponent}
        />
      )}
    </View>
  );
}
