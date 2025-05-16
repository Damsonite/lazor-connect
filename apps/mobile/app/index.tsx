import AddBtn from '~/components/contacts/AddBtn';
import ContactList from '~/components/contacts/ContactList';
import Container from '~/components/shared/Container';

export default function Home() {
  return (
    <Container>
      <ContactList />
      <AddBtn />
    </Container>
  );
}
