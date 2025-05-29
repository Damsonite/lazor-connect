import { createContext, useContext, useState } from 'react';

interface SelectedContactContextType {
  selectedContactId: string | null;
  setSelectedContactId: (id: string | null) => void;
}

const SelectedContactContext = createContext<SelectedContactContextType | undefined>(undefined);

export function SelectedContactProvider({ children }: { children: React.ReactNode }) {
  const [selectedContactId, setSelectedContactId] = useState<string | null>(null);

  return (
    <SelectedContactContext.Provider value={{ selectedContactId, setSelectedContactId }}>
      {children}
    </SelectedContactContext.Provider>
  );
}

export function useSelectedContact() {
  const context = useContext(SelectedContactContext);
  if (context === undefined) {
    throw new Error('useSelectedContact must be used within a SelectedContactProvider');
  }
  return context;
}
