# 🤖 Chat Guide

This guide explains how to use the AI-powered chat functionality in Lazor Connect.

## Overview

The chat feature uses Google's Gemini AI to help you maintain meaningful relationships by:

- Providing personalized conversation starters
- Suggesting follow-up questions
- Helping you remember important details about your contacts
- Offering relationship-building suggestions
- Automatically detecting message language and responding in English or Spanish

## Getting Started

1. Ensure you have set up your `GEMINI_API_KEY` in the backend `.env` file
2. The chat feature is automatically available when you interact with a contact

## Features

### Conversation Starters

The AI generates personalized conversation starters based on:

- Known interests and hobbies
- Recent events or updates
- Previous conversation topics
- Relationship context

Example:

```text
"I remember you enjoy landscape photography. What draws you to capturing nature's beauty? I'd love to hear about your favorite shot and the story behind it."
```

### Follow-up Questions

The AI suggests thoughtful follow-up questions to:

- Deepen the conversation
- Show genuine interest
- Learn more about your contact
- Build stronger connections

### Profile Building

The chat helps you build rich contact profiles by:

- Extracting information from conversations
- Suggesting important details to remember
- Organizing information into relevant categories
- Updating contact information automatically

### Relationship Insights

The AI provides insights about:

- Interaction patterns
- Conversation topics
- Relationship strength indicators
- Suggested contact frequency

### Multilingual Support

The AI automatically detects the language of your messages and responds accordingly:

- **English**: Send messages in English to receive responses in English
- **Spanish**: Send messages in Spanish (e.g., "Hablé con él hoy") to receive responses in Spanish
- **Automatic Detection**: No need to manually set language preferences - the AI detects based on your message content
- **Natural Switching**: You can switch between languages naturally in different conversations

## Best Practices

1. **Be Specific**: Share details about your interactions to help the AI provide better suggestions
2. **Update Regularly**: Keep contact information current for more relevant suggestions
3. **Use Follow-ups**: Take advantage of suggested follow-up questions to deepen conversations
4. **Provide Context**: Share the outcome of conversations to improve future suggestions

## Technical Details

The chat functionality is implemented using:

- Google's Gemini AI for natural language processing
- FastAPI backend for handling requests
- Secure API communication between mobile and backend
- Local storage for conversation history

## Privacy & Security

- All conversations are processed locally
- Contact information is stored securely in Supabase
- No conversation data is shared with third parties
- You can delete conversation history at any time

## Troubleshooting

If you encounter issues with the chat:

1. Check your internet connection
2. Verify your `GEMINI_API_KEY` is correctly set
3. Ensure the backend server is running
4. Check the mobile app's connection to the backend

For additional help, please open an issue on GitHub.
