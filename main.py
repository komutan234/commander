import argparse
import yaml
import time
import logging
from src.orchestrator import Orchestrator
from src.utils.logger import setup_logging

# Setup global logging
setup_logging()
logger = logging.getLogger(__name__)

def load_config(config_path):
    """Loads the main YAML configuration file."""
    logger.info(f"Loading configuration from: {config_path}")
    try:
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        return config
    except FileNotFoundError:
        logger.error(f"Configuration file not found at {config_path}")
        exit(1)
    except Exception as e:
        logger.error(f"Error parsing YAML config: {e}")
        exit(1)

def main():
    """Main entry point for the Commander service."""
    parser = argparse.ArgumentParser(description="Commander Temporal Orchestrator")
    parser.add_argument(
        "--config",
        type=str,
        default="config.yaml",
        help="Path to the configuration file."
    )
    parser.add_argument(
        "--mode",
        type=str,
        default="run",
        choices=["run", "simulate", "test_quantum_link"],
        help="Operation mode (run, simulate, or test)."
    )
    args = parser.parse_args()

    config = load_config(args.config)
    
    logger.info("Initializing Commander Orchestrator...")
    orchestrator = Orchestrator(config)

    if args.mode == "run":
        logger.info("Starting real-time orchestration loop...")
        orchestrator.start_realtime_loop()
    elif args.mode == "simulate":
        logger.info("Starting simulation mode...")
        orchestrator.run_simulation(steps=100)
    elif args.mode == "test_quantum_link":
        logger.info("Testing Quantum State link...")
        orchestrator.test_quantum_link()
    
    logger.info("Commander process finished.")

if __name__ == "__main__":
    main()
