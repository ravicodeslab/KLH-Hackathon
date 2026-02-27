# demo/seed_demo.py
import json
import os
import logging

logger = logging.getLogger(__name__)

class DemoSeeder:
    def __init__(self):
        # Dynamically locate the mock_data.json relative to this script
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.mock_file_path = os.path.join(self.base_dir, "mock_data.json")

    def load_demo_data(self):
        """
        Reads the mock_data.json and returns it as a dictionary.
        This provides zero-latency results for the frontend.
        """
        try:
            if not os.path.exists(self.mock_file_path):
                logger.error(f"❌ Demo Error: {self.mock_file_path} not found.")
                return None

            with open(self.mock_file_path, "r") as file:
                data = json.load(file)
                logger.info("✅ Demo Mode: Mock data injected successfully.")
                return data
        except Exception as e:
            logger.error(f"❌ Demo Error: Failed to parse mock data - {str(e)}")
            return None

# Create a singleton instance for the backend to use
seeder = DemoSeeder()