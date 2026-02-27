import os
import sys
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

# --- MANDATORY PATH INJECTION ---
# This finds the 'shadowtrace' folder regardless of how you run the script
current_dir = os.path.dirname(os.path.abspath(__file__)) # .../backend/app
root_path = os.path.abspath(os.path.join(current_dir, "../../")) # .../shadowtrace

if root_path not in sys.path:
    sys.path.insert(0, root_path)

# Load .env from root
load_dotenv(os.path.join(root_path, ".env"))

# Now we import using the absolute path from root
from backend.app.routers import scan
# --------------------------------

app = FastAPI(
    title="ShadowTrace OSINT Engine",
    description="AI-Powered Digital Footprint & DPDP Compliance Platform",
    version="1.0.0"
)

# CORS CONFIGURATION
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allows all origins to prevent connection errors with React
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# INCLUDE ROUTERS
app.include_router(scan.router, prefix="/api/v1")

@app.get("/")
async def root():
    return {
        "status": "online",
        "message": "ShadowTrace Backend is Live",
        "root_path": root_path
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.app.main:app", host="127.0.0.1", port=8000, reload=True)