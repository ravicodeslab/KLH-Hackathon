import sys
import os
from fastapi import APIRouter, HTTPException
import asyncio
import logging

# --- PATH INJECTION FOR ROUTER ---
current_dir = os.path.dirname(os.path.abspath(__file__)) # .../backend/app/routers
root_path = os.path.abspath(os.path.join(current_dir, "../../../")) # .../shadowtrace

if root_path not in sys.path:
    sys.path.insert(0, root_path)

# NOW IMPORTS ARE SAFE
try:
    from demo.seed_demo import seeder
    from ai.pii_detector import detector
    from ai.risk_scorer import scorer
    from compliance.dpdp_checker import checker
except ImportError as e:
    print(f"CRITICAL IMPORT ERROR: {e}")
    # This happens if __init__.py files are missing in demo/ai/compliance folders

from backend.app.scrapers.github_scraper import scan_github
from backend.app.scrapers.hibp import scan_hibp
from backend.app.scrapers.reddit_scraper import scan_reddit
from backend.app.scrapers.pastebin_scraper import scan_pastebin
from backend.app.models.schemas import ScanRequest, ScanResponse

router = APIRouter(prefix="/scan", tags=["Scanning Engine"])
logger = logging.getLogger(__name__)

@router.post("/", response_model=ScanResponse)
async def start_new_scan(request: ScanRequest):
    target_email = request.target_email.lower()
    
    # 1. DEMO TRIGGER
    if target_email == "demo@tracepoint.com":
        return seeder.load_demo_data()

    # 2. LIVE SCRAPING
    tasks = [
        scan_github(target_email),
        scan_hibp(target_email),
        scan_pastebin(target_email),
        scan_reddit(target_email.split('@')[0])
    ]
    raw_results = await asyncio.gather(*tasks)
    exposures = [res for res in raw_results if res is not None]

    # 3. AI & COMPLIANCE ENRICHMENT
    all_findings = []
    for exp in exposures:
        ai_findings = detector.scan_text(exp.get("description", ""))
        if ai_findings:
            exp["risk_level"] = "CRITICAL"
            for finding in ai_findings:
                exp["pii_found"].append(f"{finding['data_category']}: {finding['match']}")
                all_findings.append(finding)
            
            # Add DPDP violations
            violations = checker.analyze_findings(ai_findings)
            exp["compliance_notes"] = [v["section"] for v in violations]

    # 4. FINAL SCORE
    final_score = scorer.calculate(all_findings)

    return {
        "target": target_email,
        "total_leaks": len(exposures),
        "risk_score": final_score,
        "exposures": exposures
    }