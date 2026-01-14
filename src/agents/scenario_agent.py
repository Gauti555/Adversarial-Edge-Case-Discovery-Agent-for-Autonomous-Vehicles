import openai
import json
import random
from src.config import Config
from src.utils.logger import log_info, log_error

class ScenarioAgent:
    def __init__(self):
        # Verification check
        if not Config.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY not found! Run: export OPENAI_API_KEY='your_key'")

        # Initialize official OpenAI client
        self.client = openai.OpenAI(api_key=Config.OPENAI_API_KEY)
        self.template_path = "data/templates/cut_in.xml"

    def generate_scenario_parameters(self, failure_history: list) -> dict:
        recent_history = failure_history[-10:]
        history_text = "\n".join([
            f"- Run {i+1}: Ego {h['ego_speed']}km/h, Offset {h['offset']}m -> TTC: {h['ttc']}s"
            for i, h in enumerate(recent_history)
        ])

        prompt = f"""
        SYSTEM ROLE: Adversarial Autonomous Vehicle Test Engineer.
        TASK: Generate the next 'Cut-In' scenario parameters to find a collision.
        
        HISTORY:
        {history_text if history_text else "First run."}

        OUTPUT REQUIREMENTS:
        Return ONLY a JSON object:
        - "ego_speed": float (60-120)
        - "adversary_speed": float (60-130)
        - "lateral_offset": float (1-10)
        - "lane_change_duration": float (1-5)
        - "road_condition": string ("clear", "rainy", "snowy")
        """

        try:
            log_info(f" [Writer] Requesting scenario from OpenAI ({Config.MODEL_NAME})...")

            response = self.client.chat.completions.create(
                model=Config.MODEL_NAME,
                messages=[
                    {"role": "system", "content": "You are a safety tester. You output ONLY JSON."},
                    {"role": "user", "content": prompt}
                ],
                response_format={ "type": "json_object" }
            )
            
            params = json.loads(response.choices[0].message.content)
            return {
                "ego_speed": float(params.get("ego_speed", 80.0)),
                "lateral_offset": float(params.get("lateral_offset", 5.0)),
                "adversary_speed": float(params.get("adversary_speed", 85.0)),
                "lane_change_duration": float(params.get("lane_change_duration", 3.0)),
                "road_condition": params.get("road_condition", "clear")
            }
            
        except Exception as e:
            log_error(f" OpenAI API Error: {e}. Falling back to random adaptive.")
            return self._get_fallback_params(failure_history)

    def _get_fallback_params(self, failure_history: list) -> dict:
        return {
            "ego_speed": random.uniform(90.0, 110.0),
            "adversary_speed": random.uniform(100.0, 120.0),
            "lateral_offset": random.uniform(1.5, 3.5),
            "lane_change_duration": random.uniform(1.0, 2.5),
            "road_condition": "rainy"
        }

    def create_openscenario_xml(self, params: dict) -> str:
        with open(self.template_path, 'r') as f:
            return f.read().format(**params)