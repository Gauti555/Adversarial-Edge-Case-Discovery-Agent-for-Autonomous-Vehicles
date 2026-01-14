import time
import os
import random # Used for mock fallback in run_simulation for now
from src.config import Config
from src.simulator.base_adapter import BaseSimulator
from src.utils.logger import log_info, log_error, log_warning

# --- CONDITIONAL CARLA IMPORT ---
try:
    # This import will only succeed if the CARLA Python API is installed/in the path
    import carla 
    CARLA_AVAILABLE = True
except ImportError:
    CARLA_AVAILABLE = False
    log_warning("CARLA Python API not found. CarlaSimulator functionality will be limited/fail if USE_MOCK_SIMULATOR=False.")
    

class CarlaSimulator(BaseSimulator):
    """
    Real-world adapter for CARLA using the Client API and ScenarioRunner.
    """
    def __init__(self):
        if not CARLA_AVAILABLE:
            log_error("Cannot initialize CarlaSimulator: 'carla' module not installed.")
            # We don't raise an exception here, but ensure connect() fails if called
        self.client = None
        self.world = None
        self.current_scenario_path = None
        self.actors_to_destroy = []

    def connect(self):
        if not CARLA_AVAILABLE:
            return False # Exit early if module is missing
            
        try:
            log_info(f" [CARLA SIM] Connecting to CARLA at {Config.CARLA_HOST}:{Config.CARLA_PORT}...")
            self.client = carla.Client(Config.CARLA_HOST, Config.CARLA_PORT)
            self.client.set_timeout(Config.SIMULATION_TIMEOUT)
            self.world = self.client.get_world()
            log_success(" [CARLA SIM] Connection successful.")
            return True
        except Exception as e:
            log_error(f" [CARLA SIM] Failed to connect: {e}")
            log_warning(" [CARLA SIM] Please ensure the CARLA server is running.")
            return False

    def load_scenario(self, xml_content: str):
        if not self.world:
            if not self.connect():
                raise ConnectionError("CARLA connection failed during scenario load.")
        
        # 1. Save the XML string to a temporary file
        temp_file_name = f"temp_scenario_{int(time.time())}.xosc"
        temp_path = os.path.join("data", temp_file_name)
        with open(temp_path, "w") as f:
            f.write(xml_content)
        self.current_scenario_path = temp_path
        log_info(f" [CARLA SIM] Saved scenario to temporary file: {temp_path}")

    def run_simulation(self):
        if not self.current_scenario_path:
            raise Exception("No scenario loaded before run_simulation call.")

        # --- Placeholder for real CARLA monitoring loop ---
        log_warning(" [CARLA SIM] Placeholder: Running simplified mock metric generation...")
        
        # In a real setup, this would calculate TTC from sensor data
        did_collide = random.random() < 0.05 
        real_ttc = round(random.uniform(0.5, 5.0), 2)
        
        os.remove(self.current_scenario_path)

        return {
            "min_ttc": real_ttc,
            "collision": did_collide,
            "duration": 15.0 
        }

    def cleanup(self):
        log_info(" [CARLA SIM] Destroying actors and resetting world...")
        if self.client and self.actors_to_destroy:
             # Placeholder for real CARLA destruction logic
             pass 
        log_success(" [CARLA SIM] Cleanup complete.")