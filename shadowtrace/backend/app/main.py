from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import routers (Assuming they will be created next in the routers/ folder)
# We use try-except here so the app doesn't crash if you haven't created the router files yet.
try:
    from app.routers import scan, report
    routers_loaded = True
except ImportError:
    routers_loaded = False

# Initialize FastAPI App
app = FastAPI(
    title="TracePoint API",
    description="Automated OSINT & Privacy Sentinel for PS-64",
    version="1.0.0"
)

# Configure CORS (Critical for connecting with React frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins during local hackathon development
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

# Root Health Check Endpoint
@app.get("/", tags=["Health"])
async def root():
    return {
        "status": "online",
        "message": "TracePoint Backend is running successfully.",
        "routers_loaded": routers_loaded
    }

# Include Routers (if they exist)
if routers_loaded:
    app.include_router(scan.router, prefix="/api/v1")
    app.include_router(report.router, prefix="/api/v1")