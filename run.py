import uvicorn
import os
import sys

if __name__ == "__main__":
    # Force the current directory into the python path
    path = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, path)
    
    print("🛡️ ShadowTrace OSINT Engine Starting...")
    print(f"📍 Root Path: {path}")
    
    uvicorn.run(
        "backend.app.main:app", 
        host="127.0.0.1", 
        port=8000, 
        reload=True,
        log_level="info"
    )