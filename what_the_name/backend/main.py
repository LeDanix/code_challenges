from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import name_parser

app = FastAPI(title="Name and Surname Parser API", version="0.1.0")

# Middleware de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(name_parser.router)
