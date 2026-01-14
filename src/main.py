import os
import csv
from rich.table import Table
from rich.console import Console

from src.config import Config
from src.utils.logger import log_info, log_error, log_success
from src.agents.scenario_agent import ScenarioAgent
from src.agents.metric_agent import FailureMetricAgent
from src.simulator.base_adapter import BaseSimulator
from src.simulator.mock_adapter import MockSimulator
from src.simulator.carla_adapter import CarlaSimulator

from src.utils.logger import log_info, log_error, log_success, log_warning # <--- ADD log_warning
# --- Initialization ---
console = Console()
LOG_FILE = os.path.join("data", "logs", "experiment_log.csv")

def setup_simulator(use_mock: bool) -> BaseSimulator:
    """Selects and connects the appropriate simulator."""
    if use_mock:
        sim = MockSimulator()
    else:
        sim = CarlaSimulator()
    
    try:
        sim.connect()
        return sim
    except ConnectionError:
        log_error("Could not connect to the simulator. Exiting.")
        exit()

def log_experiment_data(data: dict):
    """Appends simulation results to the CSV log file."""
    file_exists = os.path.isfile(LOG_FILE)
    with open(LOG_FILE, 'a', newline='') as f:
        fieldnames = data.keys()
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        
        if not file_exists or os.path.getsize(LOG_FILE) == 0:
            writer.writeheader()
        writer.writerow(data)

def run_evaluation_loop(sim_engine: BaseSimulator, writer_agent: ScenarioAgent, judge_agent: FailureMetricAgent):
    """
    The core closed-loop feedback mechanism (ReAct Loop).
    """
    failure_history = []
    found_edge_cases = 0

    for i in range(Config.MAX_ITERATIONS):
        log_info(f"\n--- Iteration {i+1} / {Config.MAX_ITERATIONS} ---")

        # 1. REASONING & PLAN (Scenario Agent)
        params = writer_agent.generate_scenario_parameters(failure_history)
        
        # 2. ACTION (Scenario Agent generates executable script)
        xml_script = writer_agent.create_openscenario_xml(params)
        
        # 3. EXECUTION (Simulator runs the test)
        sim_engine.load_scenario(xml_script)
        sim_results = sim_engine.run_simulation()
        
        # 4. EVALUATION (Metric Agent judges the result)
        score, status = judge_agent.evaluate(sim_results)

        # 5. FEEDBACK & LOGGING
        
        # Compile all data for logging and feedback
        run_data = {
            "iteration": i + 1,
            "ego_speed": params['ego_speed'],
            "lateral_offset": params['lateral_offset'],
            "road_condition": params['road_condition'],
            "min_ttc": sim_results['min_ttc'],
            "score": score,
            "status": status
        }
        log_experiment_data(run_data)

        # Update failure history for the LLM's next reasoning step
        # Only provide key risk parameters and the result score
        feedback_entry = {
            "ego_speed": params['ego_speed'],
            "adv_speed": params['adversary_speed'],
            "offset": params['lateral_offset'],
            "duration": params['lane_change_duration'],
            "ttc": sim_results['min_ttc'],
            "score": score
        }
        failure_history.append(feedback_entry)

        if score > 0.0:
            log_warning(f" 🚨 FAILURE DETECTED: {status} (Score: {score:.2f})")
            # Save the discovered critical scenario XML
            output_file = os.path.join("data", "results", f"edge_case_{i+1}_score{score:.2f}.xosc")
            with open(output_file, "w") as f:
                f.write(xml_script)
            log_success(f"   [Saved] Critical scenario saved to {output_file}")
            found_edge_cases += 1
        else:
            log_info(f" 🟢 Result: {status}. Moving to next adversarial test.")
            
    return found_edge_cases

def generate_final_report(results_found: int):
    """Reads the log file and prints a summary table."""
    log_info("\n--- Generating Final Report ---")
    
    if not os.path.exists(LOG_FILE):
        log_error("Log file not found.")
        return

    table = Table(title=f"Edge Case Discovery Summary (Found: {results_found})")
    table.add_column("Iter.", style="dim")
    table.add_column("Scenario", style="cyan")
    table.add_column("TTC (s)", justify="right", style="yellow")
    table.add_column("Score", justify="right", style="magenta")
    table.add_column("Status", style="bold")

    with open(LOG_FILE, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            status_style = "bold red" if float(row['score']) > 0.0 else "dim green"
            table.add_row(
                row['iteration'],
                f"S:{row['ego_speed']} O:{row['lateral_offset']} C:{row['road_condition']}",
                row['min_ttc'],
                f"{float(row['score']):.2f}",
                row['status'],
                style=status_style
            )

    console.print(table)


if __name__ == "__main__":
    # Ensure log and results directories exist
    os.makedirs(os.path.join("data", "logs"), exist_ok=True)
    os.makedirs(os.path.join("data", "results"), exist_ok=True)

    # Clear previous log file for a clean experiment run
    if os.path.exists(LOG_FILE):
        os.remove(LOG_FILE)

    sim_engine = setup_simulator(Config.USE_MOCK_SIMULATOR)
    writer_agent = ScenarioAgent()
    judge_agent = FailureMetricAgent()

    found_count = run_evaluation_loop(sim_engine, writer_agent, judge_agent)
    sim_engine.cleanup()
    
    generate_final_report(found_count)
    log_success("Project Run Complete.")