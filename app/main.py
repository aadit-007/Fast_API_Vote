from datetime import datetime
from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
from .import models
from .database import engine
from .routers import post, user, auth, vote


# models.Base.metadata.create_all(bind=engine)
# making tabel is done by alembic

app = FastAPI()

origins = ["*"]
# Allow all origins for development (be more restrictive in production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Root endpoint with CORS headers
@app.get("/", response_model=dict)
async def root():
    return {
        "message": "Welcome to the FastAPI Backend!",
        "status": "running",
        "docs": "/docs",
        "timestamp": datetime.utcnow().isoformat()
    }

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)



