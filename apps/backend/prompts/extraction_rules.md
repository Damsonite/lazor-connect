# Extraction Rules

1. If a message mentions liking something (e.g., 'likes apples', 'enjoys hiking', 'loves reading'), ALWAYS add it to BOTH 'interests' array AND 'preferences.likes' array.
2. Look for phrases like 'likes', 'enjoys', 'loves', 'is into', 'is passionate about', 'prefers' as signals for interests/likes.
3. Extract specific items (e.g., 'apples' from 'likes apples') rather than entire phrases.
4. For third-person statements ('Tom likes apples', 'She enjoys hiking'), extract the interest/like properly.
5. For dates without a year (e.g., 'May 5'), always use the current year instead of '0000'.
6. Pay special attention to family relationships and details. Extract any mention of siblings, children, parents, etc. For example, if the message says 'He has two brothers and a sister', extract to family_details: 'Has two brothers and a sister'.
7. Pay attention to numerical information in family details, especially the number of siblings, children, etc.
8. For personality information, extract detailed descriptions mentioning emotional traits, behaviors, temperament, and character. Examples include: introversion/extroversion, anxiety levels, calm/excitable nature, how they interact socially, emotional responses to situations.
9. For personality statements, preserve context and descriptive language (e.g., 'gets nervous in large groups' rather than just 'nervous') to maintain meaningful personality insights.
10. Look for nickname references like "nickname is", "they call him/her", "goes by", "known as", etc. Extract only the actual nickname, not the whole phrase.
11. If a message mentions when the user last talked, met, chatted, or communicated with the contact (e.g., "we talked yesterday", "last time we spoke was May 10th", "I saw her last week"), extract this as the 'last_connection' property. Use ISO format (YYYY-MM-DD or full ISO datetime) if a date is clear, or return the natural language date string if not. Do not guess if the date is ambiguous.
12. If a message mentions what was discussed, talked about, or any subject of conversation (e.g., "we talked about football and movies", "our conversation was about work and travel"), extract these as an array in the 'conversation_topics' property. Only include topics that are clearly mentioned as conversation subjects.
