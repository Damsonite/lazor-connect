import { Href, Link } from 'expo-router';
import { Plus } from 'lucide-react-native';
import { useColorScheme } from 'nativewind';

import BaseBtn from '~/components/shared/BaseBtn';
import { colors } from '~/utils/colors';

export default function AddBtn({ href }: { href: Href }) {
  const { colorScheme } = useColorScheme();
  const mode = colorScheme ?? 'light';

  return (
    <Link href={href} asChild>
      <BaseBtn>
        <Plus size={32} color={colors.background[mode]} />
      </BaseBtn>
    </Link>
  );
}
