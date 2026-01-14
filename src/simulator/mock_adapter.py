import random
import time
import re
from src.simulator.base_adapter import BaseSimulator
from src.utils.logger import log_info, log_warning

class MockSimulator(BaseSimulator):
    """
    A fake simulator used for rapid testing of the LLM's reasoning loop.
    It fakes physics based on the XML parameters.
    """
    def __init__(self):
        self.current_params = {}
        self.connected = False

    def connect(self):
        log_info(" [MOCK SIM] Initializing MOCK Simulator Engine...")
        self.connected = True

    def load_scenario(self, xml_content: str):
        if not self.connected:
            self.connect()
        
        # Use regex to extract the key parameters the LLM set
        speed_match = re.search(r'name="EgoVehicleSpeed".*?value="(\d+\.?\d*)"', xml_content)
        offset_match = re.search(r'name="CutInLateralOffset".*?value="(\d+\.?\d*)"', xml_content)
        duration_match = re.search(r'name="LaneChangeDuration".*?value="(\d+\.?\d*)"', xml_content)
        
        self.current_params = {
            "ego_speed": float(speed_match.group(1)) if speed_match else 50.0,
            "lateral_offset": float(offset_match.group(1)) if offset_match else 10.0,
            "duration": float(duration_match.group(1)) if duration_match else 3.0,
        }
        log_info(f" [MOCK SIM] Scenario Loaded (Mock Params: {self.current_params})")

    def run_simulation(self):
        log_info(" [MOCK SIM] Running Mock Simulation...")
        time.sleep(0.5) # Simulate processing time

        # === MOCK PHYSICS LOGIC (The crucial part that determines failure) ===
        ego_speed_mps = self.current_params['ego_speed'] / 3.6  # km/h to m/s
        offset = self.current_params['lateral_offset']
        aggressiveness = 1.0 / self.current_params['duration'] # Higher is more aggressive
        
        # Heuristic Risk Formula: High speed + low offset + high aggressiveness = Low TTC
        # TTC is estimated by distance/relative_speed. Low TTC means high risk.
        risk_score = (ego_speed_mps * aggressiveness) / (offset + 1)
        
        # Map risk_score (0.1 to 5.0 typically) to TTC (0.0 to 10.0)
        # We aim for TTC to be low when risk is high.
        mock_ttc = max(0.1, 5.0 - risk_score + random.uniform(-1.0, 1.0))
        
        collision = mock_ttc < 0.3
        
        return {
            "min_ttc": round(mock_ttc, 2),
            "collision": collision,
            "duration": 15.0 # Mock run time
        }

    def cleanup(self):
        log_warning(" [MOCK SIM] Mock cleanup completed.")