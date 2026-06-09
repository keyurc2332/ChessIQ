# backend/main.py - COMPLETE VERSION

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base
from routes.auth import router as auth_router
from routes.games import router as games_router
from routes.analysis import router as analysis_router
from routes.prediction import router as prediction_router

# Create database tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(
    title="ChessIQ API",
    description="AI-powered chess analytics platform",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router)
app.include_router(games_router)
app.include_router(analysis_router)
app.include_router(prediction_router)

@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "ChessIQ API"}


@app.get("/health/db")
def health_check_db():
    """Check database connection"""
    try:
        from database import SessionLocal
        db = SessionLocal()
        db.execute("SELECT 1")
        db.close()
        return {"status": "connected", "database": "PostgreSQL"}
    except Exception as e:
        return {"status": "error", "message": str(e)}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)