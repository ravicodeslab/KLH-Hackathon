from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional

# ==========================================
# 1. THE REQUEST MODEL (What React sends us)
# ==========================================
class ScanRequest(BaseModel):
    # Using EmailStr ensures FastAPI automatically rejects invalid emails (like "bob@bob")
    target_email: EmailStr = Field(..., description="The primary email address to investigate.")
    
    # Username is optional. If not provided, our scan.py will guess it from the email.
    target_username: Optional[str] = Field(None, description="Optional: Known username used by the target.")

    class Config:
        json_schema_extra = {
            "example": {
                "target_email": "demo@example.com",
                "target_username": "demo_user_123"
            }
        }

# ==========================================
# 2. THE EXPOSURE MODEL (Individual Scraper Results)
# ==========================================
class ExposedData(BaseModel):
    platform: str = Field(..., description="The source of the leak (e.g., GitHub, Pastebin)")
    risk_level: str = Field(..., description="Risk severity: LOW, MEDIUM, HIGH, or CRITICAL")
    description: str = Field(..., description="Details about what was found.")
    pii_found: List[str] = Field(..., description="Array of sensitive data types found (e.g., ['Email', 'Password'])")
    url: Optional[str] = Field(None, description="Direct link to the exposed data or breach info.")

# ==========================================
# 3. THE FINAL RESPONSE MODEL (What we send back to React)
# ==========================================
class ScanResponse(BaseModel):
    target: str = Field(..., description="The target email that was scanned.")
    total_leaks: int = Field(..., description="Total number of platforms where data was found.")
    risk_score: int = Field(..., description="Calculated risk score from 0 (Safe) to 100 (Critical).")
    exposures: List[ExposedData] = Field(..., description="Detailed list of all findings.")

    class Config:
        json_schema_extra = {
            "example": {
                "target": "demo@example.com",
                "total_leaks": 2,
                "risk_score": 85,
                "exposures": [
                    {
                        "platform": "GitHub",
                        "risk_level": "HIGH",
                        "description": "Public commit history contains unmasked email.",
                        "pii_found": ["Email", "Commit History"],
                        "url": "https://github.com/search?q=demo@example.com"
                    }
                ]
            }
        }