import { Href, Link } from 'expo-router';
import { Plus } from 'lucide-react-native';

import Button from '~/components/shared/BaseBtn';

export default function AddBtn({ href }: { href: Href }) {
  return (
    <Link href={href} asChild>
      <Button className="absolute bottom-0 right-0 h-20 w-20 rounded-3xl">
        <Plus size={32} color="white" />
      </Button>
    </Link>
  );
}
