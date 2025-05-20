# Profile Data Extraction

Extract structured contact information from this message.
ONLY return data that's clearly mentioned in this exact message (not previous context).

Return a JSON object with ONLY the following properties where info is clearly present:

- nickname: Extract nickname if mentioned (e.g., "Tom's nickname is Racoon", "they call him Ace")
- birthday: Extract birthday in ISO format (YYYY-MM-DD) if mentioned. Use current year if no year specified.
- interests: Array of interests or hobbies mentioned, including things they like (e.g., if message says 'likes apples', add 'apples' to interests)
- important_dates: Array of objects with {date: 'YYYY-MM-DD', description: 'string'}
- relationship_type: String (friend, family, colleague, etc)
- preferences: {likes: [array of things they like], dislikes: [array of things they dislike]}
- family_details: String with family information - especially extract details about siblings, parents, children, spouses, and other family members. If specific numbers are mentioned (e.g., '2 brothers', 'has 3 kids'), include these details precisely.
- personality: String with personality traits, emotional characteristics, temperament, behaviors, or character traits mentioned (e.g., 'is very outgoing', 'tends to be shy in groups', 'has a calm demeanor', 'gets anxious in social settings').

Format as valid JSON only. No explanations or other text. Return empty object if no relevant information.
