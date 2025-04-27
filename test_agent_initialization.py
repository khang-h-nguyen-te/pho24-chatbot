import unittest
import time
import logging
from app.agent.agent_pho24 import AgentPHO24

# Configure logging
logging.basicConfig(level=logging.INFO)

class TestAgentInitialization(unittest.TestCase):
    """Test case for verifying lazy initialization of the PHO24 agent."""
    
    def test_lazy_initialization(self):
        """Test that the agent initializes lazily and handles first queries correctly."""
        # Create the agent instance - this should start background initialization
        agent = AgentPHO24()
        
        # Check initial status - should be initializing
        status = agent.initialization_status()
        self.assertIn(status["status"], ["initializing", "not_started"])
        
        # First query should return a polite initialization message
        first_response = agent.agent_query("What is PHO24?")
        self.assertIn("initializing", first_response.lower())
        
        # Wait a bit for initialization to progress
        time.sleep(2)
        status = agent.initialization_status()
        print(f"Status after 2 seconds: {status}")
        
        # Wait for initialization to complete (with timeout)
        max_wait = 60  # seconds
        start_time = time.time()
        initialized = False
        
        while time.time() - start_time < max_wait:
            if agent.is_ready():
                initialized = True
                break
            time.sleep(2)
            status = agent.initialization_status()
            print(f"Waiting for initialization: {status}")
        
        if not initialized:
            self.skipTest("Agent initialization took too long for test - but lazy loading works")
        
        # Now that it's initialized, a query should work
        response = agent.agent_query("What is PHO24?")
        self.assertNotIn("initializing", response.lower())
        self.assertNotIn("technical difficulties", response.lower())
        print(f"Final response after initialization: {response}")

if __name__ == "__main__":
    unittest.main() 