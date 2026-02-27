# ai/pii_detector.py
import re
from ai.regex_patterns import INDIAN_PATTERNS, CONTEXT_KEYWORDS
from ai.pii_categories import PII_CONFIG

class PIIDetector:
    def scan_text(self, text: str):
        if not text: return []
        text_lower = text.lower()
        findings = []

        for label, pattern in INDIAN_PATTERNS.items():
            matches = re.finditer(pattern, text)
            for m in matches:
                val = m.group()
                config = PII_CONFIG.get(label, {"risk": "INFO", "category": "Other"})
                
                # Check for context keywords within the text to boost confidence
                confidence = "LOW"
                if any(kw in text_lower for kw in CONTEXT_KEYWORDS.get(label, [])):
                    confidence = "HIGH"

                findings.append({
                    "data_category": config["category"],
                    "match": self.mask(val, label),
                    "risk": config["risk"],
                    "confidence": confidence,
                    "legal_note": config.get("legal_impact", "N/A"),
                    "fix_step": config.get("remediation", "Monitor for suspicious activity"),
                    "entity_type": label
                })
        return findings

    def mask(self, val, label):
        if label == "AADHAAR_ID": return f"XXXX-XXXX-{val[-4:]}"
        if label == "PAN_CARD": return f"{val[:2]}XXX{val[-2:]}"
        return val

detector = PIIDetector()