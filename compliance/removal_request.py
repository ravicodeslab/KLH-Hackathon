# compliance/removal_request.py
import datetime
import os

class RemovalRequestGenerator:
    def __init__(self):
        # Locate the template relative to this file
        self.template_path = os.path.join(os.path.dirname(__file__), "templates/removal_template.txt")

    def _load_template(self):
        """Helper to safely read the template file."""
        if not os.path.exists(self.template_path):
            return "Error: Template file missing. Please check compliance/templates/."
        with open(self.template_path, 'r') as file:
            return file.read()

    def generate_bulk_request(self, user_name, company_name, findings):
        """
        Generates a single letter for multiple PII leaks found at one source.
        'findings' should be a list of AI-detected items.
        """
        template = self._load_template()
        if "Error" in template:
            return template

        # Consolidate findings into a readable string for the letter
        pii_summary = []
        for f in findings:
            pii_summary.append(f"- {f.get('data_category')}: {f.get('match')}")
        
        pii_text = "\n".join(pii_summary)

        # Populate the template
        try:
            letter = template.format(
                company_name=company_name,
                pii_type="the following data categories", # Generalizes the intro
                masked_value=pii_text,
                user_name=user_name,
                current_date=datetime.date.today().strftime("%d %B %Y")
            )
            return letter
        except KeyError as e:
            return f"Error: Template formatting failed. Missing key: {e}"

# Global instance for easy access
generator = RemovalRequestGenerator()