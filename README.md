# Lazor Connect

## Telemática - Proyecto Final

**Nota**: Esta es una branch específica de un proyecto personal que incluye la configuración completa de Docker y Terraform para desarrollo y producción.

### Resumen del Trabajo Realizado

Este proyecto consiste en una aplicación full-stack con:

- **Backend**: FastAPI (Python) en puerto 8000
- **Frontend**: React Native/Expo compilado para web en puerto 8081
- **Base de datos**: Configuración para Supabase

### Ejecutar con Docker

```bash
# Clonar el repositorio y navegar al directorio
cd lazor-connect

# Construir y ejecutar todos los contenedores
sudo docker compose up -d

# Verificar que los servicios estén corriendo
sudo docker compose ps
```

### Acceder a la Aplicación

- **Frontend (Web)**: http://localhost:8081
- **Backend API**: http://localhost:8000

![Lazor Connect Logo](apps/frontend/assets/adaptive-icon.png)

> A full-stack application combining a FastAPI backend with a React Native (Expo) mobile app. Its goal is to promote meaningful human connections through AI-powered conversation guidance, relationship tracking, and personalized interaction suggestions.

## 🌟 Project Vision

Lazor Connect is designed to help people build and maintain more meaningful relationships in their lives. In today's digital age, it's easy to lose touch with important people or have superficial interactions. This app helps you:

- Build deeper, more authentic connections
- Remember important details about your relationships
- Have more meaningful conversations
- Stay connected with the people who matter
- Track and improve your relationship habits

## 📍 Project Status

Lazor Connect is currently in **active development**. Core functionality is working, but many features are being refined and improved. The backend is undergoing significant refactoring to improve code quality, performance, and maintainability. See the [Technical Priorities](#-technical-priorities) section for current development focus.

## 🚀 Features

### Core Functionality

- **Meaningful Contact Management**: Create and maintain rich contact profiles focused on relationship building
- **AI-Powered Conversation Guidance**: Get personalized suggestions for deeper, more meaningful conversations
- **Relationship Insights**: Track interaction patterns and relationship strength
- **Authentication**: Secure Supabase login system
- **API Communication**: Secure interaction between mobile and backend

### In Development

- **Smart Reminders**: Get timely suggestions for meaningful check-ins _(needs refinement)_
- **Emotional Intelligence**: AI-powered assistance in understanding and responding to emotional needs _(in progress)_
- **Streak Tracking**: Gamified relationship maintenance _(functional, needs UI improvements)_
- **Multilingual Support**: English and Spanish language detection _(functional, needs expansion)_

### Architecture

- **Scalable Design**: Monorepo with clear separation of concerns
- **Modern Stack**: FastAPI backend with React Native (Expo) mobile app

## 🛠️ Technologies

- **Backend**: FastAPI, Pydantic, Uvicorn, Google Gemini AI
- **Mobile**: React, React Native, Expo, Zustand, Expo Router, NativeWind (TailwindCSS)
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
- **Multilingual Support**: Automatic language detection with responses in English or Spanish
- **Streak Tracking**: Gamified relationship maintenance with motivational messaging

## 🗄️ Database Structure

The Supabase database schema includes:

- **contacts**: Core contact information, relationship data, and streak tracking (current_streak, longest_streak, last_streak_update)
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
cd apps/frontend
pnpm install
pnpm start  # starts development server
pnpm android  # run on Android
pnpm ios      # run on iOS
pnpm web      # run on Web
```

### 🔐 Environment Variables

```bash
# apps/frontend/.env
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

### Current Development Focus

- **Backend Code Refactoring**: Improve code structure, error handling, and maintainability
- **Prompt-to-Logic Migration**: Replace markdown instructions with programmatic logic where appropriate
- **Enhanced Data Validation**: Strengthen input validation and type safety across all endpoints
- **Service Layer Optimization**: Refactor services for better separation of concerns and testability
- **Smart Contact Recommendations**: AI-powered suggestions for who to reach out to based on relationship patterns
- **Interactive Reminder System**: Contextual reminders with conversation starters
- **Database Schema Optimization**: Improve database queries and add proper indexing
- **API Response Standardization**: Consistent error handling and response formats
- **Enhanced Multilingual Support**: Additional language support beyond English and Spanish
- **Testing Infrastructure**: Comprehensive unit and integration testing setup
- **Performance Optimization**: Backend performance improvements and caching strategies
- **Offline Support**: Core functionality available without internet connection

## 🔧 Technical Priorities

### Backend Refactoring Goals

- **Service Architecture**: Improve separation between business logic and data access layers
- **Prompt Management**: Convert static markdown prompts to dynamic, configurable prompt builders
- **Error Handling**: Implement comprehensive error handling with proper HTTP status codes
- **Type Safety**: Enhance Pydantic models and add stricter validation
- **Database Layer**: Optimize queries, add proper migrations, and implement connection pooling
- **Configuration Management**: Centralize configuration and environment variable handling
- **Logging & Monitoring**: Add structured logging and performance monitoring
- **API Documentation**: Enhance OpenAPI documentation with examples and better descriptions

### Code Quality Improvements

- **Testing**: Add unit tests, integration tests, and API endpoint testing
- **Code Standards**: Implement consistent coding standards and linting rules
- **Documentation**: Improve inline documentation and add architectural decision records
- **Performance**: Profile and optimize slow endpoints and database queries

## 🐛 Bugs & Feedback

If you find any issues or have suggestions, **open an Issue** on [GitHub Issues](https://github.com/lazor-connect/issues).

## 💖 Contributing

**Want to help?** Awesome! Follow these steps:

1. Fork the repository.
2. Create a new branch: `git checkout -b feature-new`.
3. Make your changes and commit: `git commit -m "Add a new feature 🚀"`.
4. Push your branch: `git push origin feature-new`.
5. Open a **Pull Request** and tell us what you improved.

## 📜 License

This project is licensed under the **MIT** license 📄.
