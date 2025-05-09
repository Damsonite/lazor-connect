# 🫂 Lazor Connect

A full-stack application with a FastAPI backend and React Native mobile app built with Expo.

## 📁 Project Structure

```plaintext
apps/
  ├── backend/      # FastAPI Python backend
  └── mobile/       # React Native mobile app (Expo)
libs/
  └── shared/       # Shared libraries/components
```

## 🛠️ Tech Stack

### 🖥️ Backend Deployment

- ⚡ FastAPI
- 🚀 Uvicorn server
- ✅ Pydantic for data validation

### 📱 Mobile App Development

- ⚛️ React Native with Expo
- 🧭 Expo Router for navigation
- 💨 NativeWind (TailwindCSS for React Native)
- 🗃️ Zustand for state management
- 🔐 Supabase for data storage and authentication

## 🚀 Getting Started

### 📋 Prerequisites

- [Node.js](https://nodejs.org/) (v18 or newer)
- [pnpm](https://pnpm.io/) package manager
- [Python](https://www.python.org/) (3.10 or newer)
- [Expo Go](https://expo.dev/client) app installed on your mobile device for testing

### 🐍 Backend Setup

1. Navigate to the backend directory:

   ```bash
   cd apps/backend
   ```

2. Create a Python virtual environment:

   ```bash
   python -m venv venv
   ```

3. Activate the virtual environment:

   ```bash
   # On Linux/macOS
   source venv/bin/activate

   # On Windows
   venv\Scripts\activate
   ```

4. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

5. Run the backend server:

   ```bash
   uvicorn main:app --reload --host 0.0.0.0
   ```

The API will be available at <http://localhost:8000> and API docs at <http://localhost:8000/docs>

### 📱 Mobile App Setup

1. Navigate to the mobile directory:

   ```bash
   cd apps/mobile
   ```

2. Install dependencies:

   ```bash
   pnpm install
   ```

3. Start the Expo development server:

   ```bash
   pnpm start
   ```

4. Run on specific platforms:

   ```bash
   # Android
   pnpm android

   # iOS
   pnpm ios

   # Web
   pnpm web
   ```

## 💻 Development Workflow

### 🖥️ Backend

- Edit `apps/backend/main.py` to modify API endpoints
- Add new dependencies to `requirements.txt`

### 📱 Mobile App

- Edit files in the `apps/mobile/app` directory to modify screens
- Use components from `apps/mobile/components`
- Manage state with Zustand in `apps/mobile/store`
- API interactions are handled in `apps/mobile/services/api.ts`
- Supabase client is configured in `apps/mobile/utils/supabase.ts`

### 🔐 Environment Variables

The mobile app uses environment variables for configuration, particularly for API endpoints:

1. Create a `.env` file in the `apps/mobile` directory:

   ```bash
   # apps/mobile/.env
   EXPO_PUBLIC_API_URL=http://192.168.x.x:8000  # Use your development machine's IP address
   ```

2. Access environment variables in your code:

   ```typescript
   const API_URL = process.env.EXPO_PUBLIC_API_URL;
   ```

> **Note**: Always add `.env` to your `.gitignore` file to prevent committing sensitive information.

## 🧹 Code Style and Linting

The mobile app includes ESLint and Prettier for code formatting:

```bash
# Check linting
pnpm lint

# Fix formatting issues
pnpm format
```

## 🚀 Deployment

### ☁️ Backend

The FastAPI app can be deployed to any Python-compatible hosting service like:

- Heroku
- AWS Lambda
- Google Cloud Run
- Digital Ocean App Platform

### 📱 Mobile App

The Expo app can be built for production using:

```bash
# Build for Android
eas build -p android

# Build for iOS
eas build -p ios
```
