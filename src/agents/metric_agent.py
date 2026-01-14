from typing import Tuple # <--- ADD THIS IMPORT
from src.config import Config
from src.utils.logger import log_info

class FailureMetricAgent:
    """
    The Judge Agent: Evaluates the simulation results against safety thresholds.
    """
    
    # CHANGE: Replace tuple[float, str] with Tuple[float, str]
    def evaluate(self, simulation_data: dict) -> Tuple[float, str]: 
        """
        Analyzes the simulation results and returns a normalized failure score and status.
        
        Args:
            simulation_data: Dictionary containing 'min_ttc' and 'collision'.
            
        Returns:
            (score, status): Normalized score (0.0=Safe to 1.0=Collision) and status message.
        """
        
        ttc = simulation_data.get('min_ttc', 999.0)
        collision = simulation_data.get('collision', False)
        
        log_info(f" [Judge] Evaluating results: TTC={ttc}s, Collision={collision}")

        if collision:
            return 1.0, "CATASTROPHIC COLLISION"
        
        # Check for near-miss failure (TTC below critical threshold)
        if ttc < Config.CRITICAL_TTC_THRESHOLD:
            # Calculate a normalized score: closer to 0 TTC means score approaches 1.0
            # Example: TTC=0.5s with Threshold=1.5s -> Score = 1.0 - (0.5/1.5) = 0.67
            score = 1.0 - (ttc / Config.CRITICAL_TTC_THRESHOLD)
            return score, "CRITICAL NEAR-MISS"
        
        return 0.0, "SAFE"