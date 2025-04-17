import logging
from typing import List, Dict, Any
from app.tools.base_tool import BaseTool
from app.services.embeddings import EmbeddingService
from app.config.env_config import config
from app.config.supabase_config import get_supabase_client

logger = logging.getLogger(__name__)

class Pho24SemanticSearchTool(BaseTool):
    """Tool for semantically searching Pho24 information using Supabase vector search."""
    
    def __init__(self):
        super().__init__(
            name="Pho24SemanticSearch",
            description="Search for information about Pho24 using semantic search. This tool is useful for answering questions about the restaurant, menu items, locations, and other information about Pho24."
        )
        self.embedding_service = EmbeddingService()
        self.supabase = get_supabase_client()
    
    def __call__(self, query: str, match_count: int = 5) -> str:
        """
        Perform semantic search for Pho24 information.
        
        Args:
            query: The user's question about Pho24
            match_count: Number of results to return (default: 5)
            
        Returns:
            Relevant information from the Pho24 knowledge base
        """
        try:
            # Generate embedding for the query
            logger.info(f"Generating embedding for query: {query}")
            query_embedding = self.embedding_service.get_embedding(query)
            
            if not query_embedding:
                logger.error("Failed to generate embedding for query")
                return "I'm sorry, I'm having trouble processing your question. Please try asking in a different way."
            
            # Call the Supabase RPC function for semantic search
            logger.info(f"Calling semantic_search_pho24 with match_count={match_count}")
            response = self.supabase.rpc(
                'semantic_search_pho24',
                {
                    'query_embedding': query_embedding,
                    'match_count': match_count
                }
            ).execute()
            
            # Process and format the results
            if not hasattr(response, 'data') or not response.data:
                logger.warning("No results found from semantic search")
                return "I don't have specific information about that. Is there something else about PHO24 I can help you with?"
            
            results = response.data
            logger.info(f"Found {len(results)} matching documents")
            
            # Format the results into a readable response
            if len(results) == 1:
                # If only one result, return its text directly
                return results[0]['text']
            else:
                # If multiple results, combine them into a comprehensive answer
                combined_text = "\n\n".join([result['text'] for result in results])
                return combined_text
                
        except Exception as e:
            logger.error(f"Error in semantic search: {e}")
            import traceback
            logger.error(traceback.format_exc())
            return "I apologize, but I'm having trouble accessing information about PHO24 at the moment. Please try again later." 