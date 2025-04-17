from typing import List
import uvicorn
from fastapi import FastAPI, HTTPException, Request
import asyncio
from concurrent.futures import ThreadPoolExecutor
import logging

# Import from our application structure
from app.agent.agent_pho24 import AgentPHO24
from app.models.request_models import QueryRequest, HealthResponse
from app.utils.response_utils import create_response
from app.config.env_config import config

# Configure logging
logging.basicConfig(
    level=logging.DEBUG if config.debug else logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Create FastAPI app
app = FastAPI(
    title="PHO24 Chatbot API",
    description="API for interacting with the PHO24 Chatbot",
    version="1.0.0"
)
executor = ThreadPoolExecutor(max_workers=4)

# Create a global agent instance
pho24_agent = AgentPHO24()

# Create logger for the FastAPI app
logger = logging.getLogger(__name__)

# A helper function to process the query synchronously
def process_query(query: str) -> str:
    """
    Process a user query using the agent.
    
    Args:
        query: The user's question
    
    Returns:
        The agent's response
    """
    response = pho24_agent.agent_query(query)
    return response
    
# Define a POST endpoint to receive user queries
@app.post("/ask")
async def ask_query(payload: QueryRequest, request: Request):
    """
    Process a user question and return the agent's response.
    
    Args:
        payload: The query request containing the user question
        request: The FastAPI request object
    
    Returns:
        The agent's response
    """
    query = payload.query
    logger.debug(f"Processing query: {query}")
    
    # Offload the blocking agent call to a thread pool to avoid blocking the event loop
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(executor, process_query, query)
    
    if not result:
        raise HTTPException(status_code=500, detail="Failed to process query")
    
    return {"response": result}

# Add a simple health check endpoint
@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Simple health check endpoint to verify the API is running."""
    return HealthResponse(status="ok", version="1.0.0")

# ------------------------------------------------------------
# Main Function
# ------------------------------------------------------------
# if __name__ == "__main__":
#     # Run the FastAPI app using uvicorn
#     uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True) 