"""Main FastAPI application."""

import os
from fastapi import FastAPI, Depends, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1 import document, hackrx
from app.core.config import settings

# Create FastAPI app
app = FastAPI(
    title="HackRx Document Processing API",
    description="LLM-Powered Intelligent Query-Retrieval System",
    version="0.1.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API Bearer Token Authentication
async def verify_token(request: Request):
    """Verify the API bearer token."""
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing Authorization header",
        )
    
    scheme, _, token = auth_header.partition(" ")
    if scheme.lower() != "bearer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication scheme",
        )
    
    if token != settings.API_BEARER_TOKEN:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )
    
    return token

# Include API routers
app.include_router(
    document.router,
    prefix="/api/v1",
    dependencies=[Depends(verify_token)],
)

# Include HackRx router
app.include_router(
    hackrx.router,
    prefix="/api/v1",
    dependencies=[Depends(verify_token)],
)

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Welcome to HackRx Document Processing API",
        "version": "0.1.0",
        "status": "online",
    }

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "api_version": "v1",
    }

# Create storage directory if it doesn't exist
@app.on_event("startup")
async def startup_event():
    """Run startup tasks."""
    os.makedirs(settings.DOCUMENT_STORAGE_PATH, exist_ok=True)
