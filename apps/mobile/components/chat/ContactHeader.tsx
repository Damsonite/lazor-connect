import { Flame } from 'lucide-react-native';
import { useColorScheme } from 'nativewind';
import { useEffect, useMemo, useState } from 'react';
import { Dimensions, ScrollView, Text, View } from 'react-native';

import ContactDetail from '~/components/chat/ContactDetail';
import { Contact } from '~/types/contact';
import { colors, withOpacity } from '~/utils/colors';
import { formatBirthday, formatRelativeTime } from '~/utils/date';

export default function ContactHeader({ contact }: { contact: Contact }) {
  const [expanded, setExpanded] = useState(false);
  const [dimensions, setDimensions] = useState(Dimensions.get('window'));
  const { colorScheme } = useColorScheme();
  const mode = colorScheme ?? 'light';

  useEffect(() => {
    const subscription = Dimensions.addEventListener('change', ({ window }) => {
      setDimensions(window);
    });

    return () => subscription?.remove();
  }, []);

  const formatRelationshipStrength = (value: number | null) => {
    if (value === null) return 'Not set';
    return `${value}/5`;
  };

  // Check if there are details to show
  const hasDetails = useMemo(() => {
    return !!(
      contact.nickname ||
      contact.last_connection ||
      contact.birthday ||
      contact.relationship_type ||
      contact.relationship_strength ||
      contact.interests ||
      contact.conversation_topics ||
      contact.family_details ||
      contact.personality
    );
  }, [contact]);

  const toggleExpanded = () => {
    setExpanded((prev) => !prev);
  };

  const isDesktop = dimensions.width >= 768;

  return (
    <View
      className={`border-b p-4 ${isDesktop ? 'h-auto min-h-16' : expanded ? 'max-h-[50%]' : 'h-auto'}`}
      style={{
        backgroundColor: withOpacity('primary', 0.05, mode),
        borderColor: withOpacity('primary', 0.1, mode),
      }}>
      <View className="flex-row items-center justify-between">
        <View className="flex-row items-center gap-2">
          <Flame size={24} color={colors.accent[mode]} />
          <Text className="font-exsemibold text-lg text-accent">{contact.current_streak || 0}</Text>
        </View>

        {hasDetails && (
          <Text
            className={`px-2 py-1 font-exmedium text-primary ${isDesktop ? 'text-base' : ''}`}
            onPress={toggleExpanded}>
            {expanded ? 'Show less' : 'Show more'}
          </Text>
        )}
      </View>

      {expanded && (
        <ScrollView className="mt-2 flex-col gap-2" showsVerticalScrollIndicator={false}>
          <ContactDetail label="Nickname" value={contact.nickname} />
          <ContactDetail
            label="Last contact"
            value={contact.last_connection}
            formatter={formatRelativeTime}
          />
          <ContactDetail label="Birthday" value={contact.birthday} formatter={formatBirthday} />
          <ContactDetail label="Relationship" value={contact.relationship_type} />
          <ContactDetail
            label="Connection strength"
            value={contact.relationship_strength}
            formatter={formatRelationshipStrength}
          />
          <ContactDetail
            label="Current streak"
            value={contact.current_streak}
            formatter={(value: number) => (value ? `${value} days` : 'No streak')}
          />
          <ContactDetail
            label="Best streak"
            value={contact.longest_streak}
            formatter={(value: number) => (value ? `${value} days` : 'No streak yet')}
          />
          <ContactDetail label="Interests" value={contact.interests} inline={false} />
          <ContactDetail
            label="Previous conversation topics"
            value={contact.conversation_topics}
            inline={false}
          />
          <ContactDetail label="Family details" value={contact.family_details} inline={false} />
          <ContactDetail label="Personality" value={contact.personality} inline={false} />
        </ScrollView>
      )}
    </View>
  );
}
