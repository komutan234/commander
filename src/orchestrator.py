import time
import logging
from .temporal_link import ChronosDBConnector
from .quantum_state import QuantumStateManager
from .rag_pipeline import RAGPipeline

logger = logging.getLogger(__name__)

class Orchestrator:
    """
    Coordinates all modules (Quantum, Temporal DB, and GenAI) to maintain
    a stable, forward-propagating quantum state.
    """

    def __init__(self, config):
        logger.info("Orchestrator initializing sub-modules...")
        self.config = config
        self.simulation_mode = config['orchestrator']['simulation_mode']
        self.tick_rate = 1.0 / config['orchestrator']['tick_rate_hz']
        
        # Initialize core components
        self.db_connector = ChronosDBConnector(config['chronosdb_config'])
        self.qsm = QuantumStateManager(config['qpu_settings'])
        self.rag_pipeline = RAGPipeline(config['genai_agent'], self.db_connector)
        
        self.current_state_vector = None
        self.is_running = True
        logger.info("Orchestrator ready.")

    def _tick(self):
        """
        Executes a single step (tick) of the orchestration logic.
        """
        try:
            # 1. Measure current quantum eigenvector
            logger.debug("Measuring quantum eigenvector...")
            eigenvector = self.qsm.measure_eigenvector()

            # 2. Query ChronosDB for temporal delta based on the measurement
            logger.debug(f"Querying ChronosDB with vector: {eigenvector}")
            temporal_data = self.db_connector.query_state(eigenvector)

            # 3. Use GenAI RAG to process data and determine next action
            logger.debug("Running RAG pipeline for next state decision...")
            next_action = self.rag_pipeline.generate_next_action(temporal_data)

            # 4. Calculate new state and commit to DB
            logger.debug("Calculating and committing new entangled state...")
            new_state = self.qsm.entangle_new_state(eigenvector, next_action)
            transaction_id = self.db_connector.commit_state(new_state)
            
            self.current_state_vector = new_state
            logger.info(f"Tick complete. New state committed: {transaction_id}")

        except Exception as e:
            logger.error(f"Error in orchestration tick: {e}")
            self.is_running = False # Halt on critical error

    def start_realtime_loop(self):
        """Runs the orchestration in a continuous loop."""
        while self.is_running:
            start_time = time.time()
            self._tick()
            elapsed = time.time() - start_time
            sleep_time = max(0, self.tick_rate - elapsed)
            time.sleep(sleep_time)

    def run_simulation(self, steps=100):
        """Runs a finite simulation for N steps."""
        for i in range(steps):
            logger.info(f"Simulation step {i+1}/{steps}")
            self._tick()
            if not self.is_running:
                logger.warning("Simulation halted early due to error.")
                break

    def test_quantum_link(self):
        """A simple test to verify QPU connection."""
        is_connected = self.qsm.health_check()
        logger.info(f"Quantum link health check: {'OK' if is_connected else 'FAILED'}")
        return is_connected
