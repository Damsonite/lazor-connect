# 🫂 Lazor Connect

> A full-stack application combining a **FastAPI** backend with a **React Native (Expo)** mobile app. Its goal is to promote meaningful human connections through AI-powered conversation guidance, relationship tracking, and personalized interaction suggestions.

## 🌟 Project Vision

Lazor Connect is designed to help people build and maintain more meaningful relationships in their lives. In today's digital age, it's easy to lose touch with important people or have superficial interactions. This app helps you:

- Build deeper, more authentic connections
- Remember important details about your relationships
- Have more meaningful conversations
- Stay connected with the people who matter
- Track and improve your relationship habits

## 🚀 Features

- **Meaningful Contact Management**: Create and maintain rich contact profiles focused on relationship building
- **AI-Powered Conversation Guidance**: Get personalized suggestions for deeper, more meaningful conversations
- **Relationship Insights**: Track interaction patterns and relationship strength
- **Smart Reminders**: Get timely suggestions for meaningful check-ins
- **Emotional Intelligence**: AI-powered assistance in understanding and responding to emotional needs
- **Authentication**: Secure Supabase login system
- **API Communication**: Secure interaction between mobile and backend
- **Scalable Architecture**: Monorepo with clear separation of concerns

## 🛠️ Technologies

- **Backend**: FastAPI, Pydantic, Uvicorn, Google Gemini AI
- **Mobile**: React Native (Expo), Zustand, Expo Router, NativeWind (TailwindCSS)
- **Database & Auth**: Supabase

## 📋 Contact Model

The application uses a rich contact model focused on meaningful relationship management:

### Basic Information

- **name**: Full contact name (required)
- **nickname**: Optional familiar name
- **birthday**: Birth date in ISO format
- **contact_methods**: List of contact methods (type, value, preferred)

### Relationship Management

- **last_connection**: When you last interacted with this person
- **avg_days_btw_contacts**: Average days between interactions
- **recommended_contact_freq_days**: How often you should connect
- **relationship_type**: Type of relationship (friend, family, colleague, etc.)
- **relationship_strength**: Connection strength (1-5 scale)

### Contextual Information

- **conversation_topics**: List of topics you usually discuss
- **important_dates**: List of significant dates with descriptions
- **reminders**: List of follow-up items with optional due dates

### Personal Details

- **interests**: List of what the person is interested in
- **family_details**: Information about family members
- **preferences**: Likes and dislikes
- **personality**: Information about the person's personality traits

## 🤖 AI-Powered Features

The app uses Google's Gemini AI to provide:

- **Meaningful Conversation Starters**: Personalized prompts that encourage deeper connection
- **Emotional Intelligence**: Suggestions for empathetic responses and support
- **Relationship Building**: Tips for strengthening connections
- **Contextual Memory**: Remembers important details about your relationships
- **Personalized Suggestions**: Tailored recommendations based on relationship history

## 🗄️ Database Structure

The Supabase database schema includes:

- **contacts**: Core contact information and relationship data
- **contact_methods**: Different ways to contact a person
- **important_dates**: Significant dates related to contacts
- **reminders**: Follow-up items for contacts
- **interactions**: Record of meaningful conversations and interactions

## ⚡Installation & Usage

### 🔧 Requirements

- Node.js v18+
- pnpm
- Python 3.10+
- Expo Go app installed on your phone or emulator

### ⚙️ Backend

```bash
cd apps/backend
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
# Make sure to set up your Supabase credentials in .env file (see Environment Variables section)
uvicorn main:app --reload --host 0.0.0.0
```

API available at [http://localhost:8000](http://localhost:8000/)

Docs at [http://localhost:8000/docs](http://localhost:8000/docs)

### 📱 Mobile App

```bash
cd apps/mobile
pnpm install
pnpm start  # starts development server
pnpm android  # run on Android
pnpm ios      # run on iOS
pnpm web      # run on Web
```

### 🔐 Environment Variables

```bash
# apps/mobile/.env
EXPO_PUBLIC_API_URL=http://192.168.x.x:8000
```

For the backend, copy the example file and update with your credentials:

```bash
# Copy the example file
cp apps/backend/.env.example apps/backend/.env
# Edit with your Supabase credentials
nano apps/backend/.env
```

The backend `.env` file should contain:

```bash
# apps/backend/.env
SUPABASE_URL=your_supabase_url_here
SUPABASE_KEY=your_supabase_key_here
GEMINI_API_KEY=your_gemini_api_key_here  # Required for chat functionality
```

### 🤖 Chat Functionality

For detailed instructions on using the AI-powered chat functionality, refer to the [Chat Guide](CHAT_GUIDE.md).

Access them in your code:

```ts
// Mobile
const API_URL = process.env.EXPO_PUBLIC_API_URL;

// Backend (Python)
supabase_url = os.getenv("SUPABASE_URL");
supabase_key = os.getenv("SUPABASE_KEY");
```

## 🎯 Roadmap

### 🔹 v1.0.0

- Functional mobile-backend connection
- Contact CRUD
- Shared state using Zustand
- Styling with NativeWind
- Functional monorepo

## 🐛 Bugs & Feedback

If you find any issues or have suggestions, **open an Issue** on [GitHub Issues](https://github.com/your_username/repo/issues).

## 💖 Contributing

**Want to help?** Awesome! Follow these steps:

1. Fork the repository.
2. Create a new branch: `git checkout -b feature-new`.
3. Make your changes and commit: `git commit -m "Add a new feature 🚀"`.
4. Push your branch: `git push origin feature-new`.
5. Open a **Pull Request** and tell us what you improved.

## 📜 License

This project is licensed under the **MIT** license 📄.
