# 🫂 Lazor Connect

> A full-stack application combining a **FastAPI** backend with a **React Native (Expo)** mobile app. Its goal is to promote meaningful human connections through reminders, suggestions, and interaction tracking.

## 🚀 Features

- **Contact Management**: Create, edit, and delete meaningful contacts.
- **Authentication**: Integrated Supabase login.
- **API Communication**: Secure interaction between mobile and backend.
- **Scalable Architecture**: Monorepo with clear separation of concerns.

## 🛠️ Technologies

- **Backend**: FastAPI, Pydantic, Uvicorn
- **Mobile**: React Native (Expo), Zustand, Expo Router, NativeWind (TailwindCSS)
- **Database & Auth**: Supabase

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
uvicorn main:app --reload --host 0.0.0.0
```

API available at [http://localhost:8000](http://localhost:8000/)

Docs at http://localhost:8000/docs

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

Access them in your code:

```
ts
CopiarEditar
const API_URL = process.env.EXPO_PUBLIC_API_URL;

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
