# ai/risk_scorer.py
from ai.pii_categories import PII_CONFIG

class RiskScorer:
    def calculate(self, findings: list) -> int:
        if not findings: return 0
        
        points = {"CRITICAL": 35, "HIGH": 20, "MEDIUM": 10, "LOW": 5}
        total = 0
        types_found = {f["entity_type"] for f in findings}
        
        for entity_type in types_found:
            risk_level = PII_CONFIG.get(entity_type, {}).get("risk", "LOW")
            total += points.get(risk_level, 5)

        # AGGRAVATING FACTOR: If both Financial and Identity data are leaked
        if "PAN_CARD" in types_found and "AADHAAR_ID" in types_found:
            total += 15 # "Identity Synthesis" risk bonus
            
        return min(total, 100)

scorer = RiskScorer()