# SchemeFlow FastAPI Application Entrypoint
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.db.seed_data import init_db_and_seed
from app.api import schemes, recommendations, assistant, profile, tracker

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Ensure tables exist and seed verified government schemes
    init_db_and_seed()
    yield

app = FastAPI(
    title="SchemeFlow API",
    description="Personalized, Explainable Government Scheme Discovery & Eligibility Assistant",
    version="1.1.0",
    lifespan=lifespan
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API Routers
app.include_router(schemes.router, prefix=settings.API_V1_STR)
app.include_router(recommendations.router, prefix=settings.API_V1_STR)
app.include_router(assistant.router, prefix=settings.API_V1_STR)
app.include_router(profile.router, prefix=settings.API_V1_STR)
app.include_router(tracker.router, prefix=settings.API_V1_STR)

@app.get("/api/health")
def health_check():
    return {
        "status": "healthy",
        "service": "SchemeFlow API",
        "version": "1.1.0",
        "verified_schemes": "Loaded",
        "features": [
            "Scheme Comparison View",
            "Application Status Tracker",
            "Near-Miss Eligibility Feedback",
            "Case Studies & Impact Metrics",
            "Deadline & Renewal Alerts",
            "Voice & Text-to-Speech Engine"
        ]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
