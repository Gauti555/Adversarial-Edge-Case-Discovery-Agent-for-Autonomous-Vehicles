
import os
from dotenv import load_dotenv

# Load .env file if it exists, but prioritize actual environment variables
load_dotenv()

class Config:
    # ==============================
    # 🤖 AI / LLM Configuration
    # ==============================
    # Pulls from 'export OPENAI_API_KEY=...'
    api_key = os.getenv("OPENAI_API_KEY")
    
    # Using official OpenAI models
    MODEL_NAME = "gpt-4o"  # Options: "gpt-4o", "gpt-4o-mini"

    # ==============================
    # 🎮 Simulation Configuration
    # ==============================
    USE_MOCK_SIMULATOR = True 
    CARLA_HOST = "127.0.0.1"
    CARLA_PORT = 2000
    SIMULATION_TIMEOUT = 20.0

    # ==============================
    # 🧪 Experiment Settings
    # ==============================
    MAX_ITERATIONS = 10
    CRITICAL_TTC_THRESHOLD = 1.5













########################   with API ####################
#import os
#from dotenv import load_dotenv




# Load environment variables from a .env file if present
#load_dotenv()

#class Config:
    # ==============================
    # 🤖 AI / LLM Configuration
    # ==============================
    # Replace with your actual API Key or set it in your OS environment variables
    
    # Model to use (gpt-4o is recommended for complex logic, gpt-3.5-turbo for cost saving)
    #MODEL_NAME = "gpt-5.1" 

    # ==============================
    # 🎮 Simulation Configuration
    # ==============================
    # Set to TRUE to run without CARLA (Fast Testing)
    # Set to FALSE to try connecting to a running CARLA server
    #USE_MOCK_SIMULATOR = True 
    
    # IP and Port where CARLA Simulator is running (Default is localhost:2000)
    #CARLA_HOST = "127.0.0.1"
    #CARLA_PORT = 2000
    
    # Timeout to wait for the simulator to respond (seconds)
    #SIMULATION_TIMEOUT = 20.0

    # ==============================
    # 🧪 Experiment Settings
    # ==============================
    # How many times should the agent try to find a failure?
    #MAX_ITERATIONS = 10
    
    # Threshold: If TTC (Time To Collision) is below this, it counts as a Critical Near-Miss
    #CRITICAL_TTC_THRESHOLD = 1.5