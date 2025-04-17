from typing import Dict, List, Optional
import logging

from llama_index.llms.openai import OpenAI as OpenAI_LLAMA
from llama_index.agent.openai import OpenAIAgent
from llama_index.core import PromptTemplate
from llama_index.core.memory.chat_memory_buffer import ChatMemoryBuffer
from llama_index.core.tools import FunctionTool

from app.templates.prompt_templates import PHO24_SYSTEM_TEMPLATE
from app.tools.search.pho24_semantic_search_tool import Pho24SemanticSearchTool
from app.config.env_config import config

 
class AgentPHO24:
    """
    PHO24 agent for answering queries about the brand.
    This agent uses semantic search to provide accurate information about PHO24.
    """
    
    def __init__(self):
        self.qa_template = PromptTemplate(PHO24_SYSTEM_TEMPLATE)
        self.gpt4_llm = OpenAI_LLAMA(model=config.llm_model)
        self.agent = None
        self._setup_agent()
        self.logger = logging.getLogger(__name__)
    
    def _setup_agent(self):
        """Set up the agent with necessary tools."""
        # Create semantic search tool
        pho24_semantic_search_tool = Pho24SemanticSearchTool()
        
        # Create llama_index FunctionTool object
        pho24_semantic_search_function_tool = FunctionTool.from_defaults(
            name=pho24_semantic_search_tool.name,
            description=pho24_semantic_search_tool.description,
            fn=pho24_semantic_search_tool.__call__
        )
        
        # Set up memory with configurable token limit
        memory = ChatMemoryBuffer.from_defaults(token_limit=config.memory_token_limit)
        
        # Initialize agent with tools
        self.agent = OpenAIAgent.from_tools(
            tools=[pho24_semantic_search_function_tool],
            llm=self.gpt4_llm,
            memory=memory,
            verbose=True,
            system_prompt=PHO24_SYSTEM_TEMPLATE
        )
    
    def agent_query(self, query: str) -> str:
        """
        Query the agent with a user question.
        
        Args:
            query: The user's question.
            
        Returns:
            The agent's response.
        """
        try:
            response = self.agent.chat(query)
            return str(response)
        except Exception as e:
            self.logger.error(f"Error querying agent: {e}")
            # Return a fallback response in case of an error
            if any(char in query for char in "àáảãạăắằẳẵặâấầẩẫậèéẻẽẹêếềểễệìíỉĩịòóỏõọôốồổỗộơớờởỡợùúủũụưứừửữựỳýỷỹỵđ"):
                return "Tôi xin lỗi, hiện tại tôi gặp vấn đề kỹ thuật. Vui lòng thử lại sau hoặc liên hệ với chúng tôi qua website của PHO24."
            else:
                return "I apologize, I'm currently experiencing technical difficulties. Please try again later or contact us through the PHO24 website." 