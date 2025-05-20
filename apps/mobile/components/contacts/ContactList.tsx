import ContactItem from '~/components/contacts/ContactItem';
import BaseList from '~/components/shared/BaseList';
import { getContacts } from '~/services/contactService';
import { Contact } from '~/types/contact';

export default function ContactList() {
  return (
    <BaseList<Contact>
      fetchData={getContacts}
      renderItem={({ item }) => <ContactItem contact={item} />}
      emptyMessage="No contacts found. Add your first contact!"
    />
  );
}
