from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.core.config import settings
from app.services.database import mongodb
from app.routers import heritage

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Connect to MongoDB
    mongodb.connect()
    yield
    # Shutdown: Close MongoDB connection
    mongodb.close()

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8501", "http://192.168.1.2:8501"],  # Streamlit addresses
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(heritage.router, prefix=settings.API_PREFIX)

@app.get("/")
async def root():
    return {"message": "Welcome to Heritage Virtual Guide API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "database": "connected" if mongodb.client else "disconnected"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)