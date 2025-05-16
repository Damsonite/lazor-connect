from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import contacts, health

app = FastAPI(
    title="Lazor Connect API",
    description="API for managing contacts in Lazor Connect",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(contacts.router)
