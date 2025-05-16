import { Link } from 'expo-router';

import { Button } from '~/components/Button';
import { Container } from '~/components/Container';

export default function Home() {
  return (
    <Container>
      <Link href="/contact/create" asChild>
        <Button title="Añadir contacto" />
      </Link>
    </Container>
  );
}
