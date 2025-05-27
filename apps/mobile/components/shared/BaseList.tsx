import { FlashList, ListRenderItem } from '@shopify/flash-list';
import { useEffect, useState } from 'react';
import { View } from 'react-native';

import Empty from '~/components/shared/Empty';
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
  const [error, setError] = useState<string | undefined>(undefined);

  const loadData = async () => {
    if (!fetchData) return;

    setLoading(true);
    setError(undefined);

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

  return (
    <View className="flex-1 ">
      <LoadingIndicator loading={loading} error={error} />
      {!loading && !error && (
        <FlashList
          data={data}
          renderItem={renderItem}
          estimatedItemSize={80}
          onRefresh={loadData}
          refreshing={loading}
          ListEmptyComponent={() => <Empty message={emptyMessage} />}
        />
      )}
    </View>
  );
}
