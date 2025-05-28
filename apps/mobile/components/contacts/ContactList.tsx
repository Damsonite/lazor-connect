import ContactItem from '~/components/contacts/ContactItem';
import BaseList from '~/components/shared/BaseList';
import { getContacts } from '~/services/contactService';
import { Contact } from '~/types/contact';

interface ContactListProps {
  isSidebar?: boolean;
}

export default function ContactList({ isSidebar = false }: ContactListProps) {
  return (
    <BaseList<Contact>
      fetchData={getContacts}
      renderItem={({ item }) => <ContactItem contact={item} isSidebar />}
      emptyMessage="No contacts found. Add your first contact!"
      className={isSidebar ? 'mx-4' : ''}
      showVerticalScrollIndicator={false}
    />
  );
}
