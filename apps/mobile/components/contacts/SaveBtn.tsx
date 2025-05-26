import { Save } from 'lucide-react-native';
import { useColorScheme } from 'nativewind';

import BaseBtn from '~/components/shared/BaseBtn';
import { colors } from '~/utils/colors';

interface SaveBtnProps {
  onPress: () => void;
  disabled?: boolean;
}

export default function SaveBtn({ onPress, disabled }: SaveBtnProps) {
  const { colorScheme } = useColorScheme();
  const mode = colorScheme ?? 'light';

  return (
    <BaseBtn onPress={onPress} isAction disabled={disabled} className="p-4" color="primary">
      <Save size={32} color={colors.background[mode]} />
    </BaseBtn>
  );
}
