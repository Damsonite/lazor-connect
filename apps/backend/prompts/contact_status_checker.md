# Contact Status Checker Instructions

Check the contact's last_connection and recommended_contact_freq_days to determine their contact status.

## Status Categories

### OVERDUE (Priority 1)
- Last contact was more than recommended_contact_freq_days ago
- OR no last_connection recorded
- Response: Strongly motivate to contact TODAY

### DUE_TODAY (Priority 2) 
- Last contact was exactly recommended_contact_freq_days ago
- Response: Encourage to reach out today

### RECENT_BUT_CHECK (Priority 3)
- Last contact was yesterday or 1-2 days ago
- Response: Ask if they've contacted them today

### CONTACTED_TODAY (Priority 4)
- Last contact was today
- Response: Celebrate and ask for details

## Output Format

Return JSON with:
```json
{
  "status": "OVERDUE|DUE_TODAY|RECENT_BUT_CHECK|CONTACTED_TODAY",
  "days_since_contact": number,
  "recommended_frequency": number,
  "message_type": "motivate|check|celebrate",
  "urgency_level": "high|medium|low"
}
```

## Calculation Logic

```
days_since_contact = today - last_connection
recommended_freq = recommended_contact_freq_days || 7

if days_since_contact == 0: CONTACTED_TODAY
elif days_since_contact >= recommended_freq: OVERDUE
elif days_since_contact == recommended_freq - 1: DUE_TODAY  
elif days_since_contact <= 2: RECENT_BUT_CHECK
else: OVERDUE
```
