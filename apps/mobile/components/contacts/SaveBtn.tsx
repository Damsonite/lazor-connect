import { Save } from 'lucide-react-native';

import BaseBtn from '~/components/shared/BaseBtn';

interface SaveBtnProps {
  onPress: () => void;
}

export default function SaveBtn({ onPress }: SaveBtnProps) {
  return (
    <BaseBtn className="absolute bottom-0 right-0 h-20 w-20 rounded-3xl" onPress={onPress}>
      <Save size={32} color="white" />
    </BaseBtn>
  );
}
