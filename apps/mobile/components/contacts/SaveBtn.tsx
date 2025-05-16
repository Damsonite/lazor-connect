import { Save } from 'lucide-react-native';

import Button from '~/components/shared/Button';

interface SaveBtnProps {
  onPress: () => void;
}

export default function SaveBtn({ onPress }: SaveBtnProps) {
  return (
    <Button className="absolute bottom-0 right-0 h-20 w-20 rounded-3xl" onPress={onPress}>
      <Save size={32} color="white" />
    </Button>
  );
}
