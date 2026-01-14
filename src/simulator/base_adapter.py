from abc import ABC, abstractmethod

class BaseSimulator(ABC):
    """
    Abstract Base Class defining the required interface for any simulator.
    """
    @abstractmethod
    def connect(self):
        """Initializes connection to the simulator."""
        pass

    @abstractmethod
    def load_scenario(self, xml_content: str):
        """Loads and prepares the scenario from the OpenSCENARIO XML string."""
        pass
    
    @abstractmethod
    def run_simulation(self):
        """
        Executes the scenario and returns the final metrics.

        Returns:
            dict: Must include 'min_ttc' (float) and 'collision' (bool).
        """
        pass

    @abstractmethod
    def cleanup(self):
        """Destroys all spawned actors and resets the world state."""
        pass