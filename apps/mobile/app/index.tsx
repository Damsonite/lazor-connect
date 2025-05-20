import ContactList from '~/components/contacts/ContactList';
import AddBtn from '~/components/shared/AddBtn';
import Container from '~/components/shared/Container';

export default function Home() {
  return (
    <Container>
      <ContactList />
      <AddBtn href="/contact/create" />
    </Container>
  );
}
