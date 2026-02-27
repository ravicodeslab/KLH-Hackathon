# compliance/dpdp_checker.py

class DPDPChecker:
    def __init__(self):
        # Mapping Data Categories to specific DPDP Act Violations
        # This acts as a high-speed lookup table
        self.compliance_map = {
            "AADHAAR_ID": {
                "section": "Section 8(5)",
                "violation": "Breach of Security Safeguards",
                "clause": "Fiduciaries must protect personal data in its custody by taking reasonable security safeguards.",
                "penalty": "Up to ₹250 Crores"
            },
            "PAN_CARD": {
                "section": "Section 11",
                "violation": "Right to Data Portability/Erasure",
                "clause": "Financial data exposed without active consent or purpose limitation.",
                "penalty": "Significant administrative fines"
            },
            "PRIVATE_KEY": {
                "section": "Section 8(1)",
                "violation": "General Obligation of Data Fiduciary",
                "clause": "Failure to ensure the accuracy and safety of sensitive security credentials.",
                "penalty": "Case-specific high-impact fines"
            }
        }
        
        # Default fallback for general data like Email or Phone
        self.default_violation = {
            "section": "Section 12",
            "violation": "Right to Correction and Erasure",
            "clause": "Data principal has the right to seek erasure of data that is no longer necessary.",
            "penalty": "Standard compliance penalties"
        }

    def analyze_findings(self, ai_findings: list):
        """
        Efficiently maps AI-detected PII to legal DPDP violations.
        """
        if not ai_findings:
            return []

        compliance_report = []
        # Use a set to track unique sections so we don't repeat the same legal advice
        seen_sections = set()

        for finding in ai_findings:
            entity = finding.get("entity_type")
            legal_info = self.compliance_map.get(entity, self.default_violation)
            
            # Check if we've already added this specific section to the report
            if legal_info["section"] not in seen_sections:
                compliance_report.append({
                    "data_type": finding.get("data_category", "General Data"),
                    "masked_value": finding.get("match"),
                    **legal_info
                })
                seen_sections.add(legal_info["section"])

        return compliance_report

# Initialize the checker
checker = DPDPChecker()