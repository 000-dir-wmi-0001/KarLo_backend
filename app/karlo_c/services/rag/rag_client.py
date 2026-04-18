"""
RAG App Client - Handles communication with the RAG service
"""
import httpx
import logging
from typing import Optional
from app.core.config import settings

logger = logging.getLogger(__name__)


class RAGClient:
    """Client for communicating with RAG App endpoint"""
    
    def __init__(self, base_url: Optional[str] = None, timeout: int = 30):
        self.base_url = base_url or settings.RAG_APP_ENDPOINT
        self.timeout = timeout
        
    async def ask(self, query: str, user_id: str) -> dict:
        """
        Send a query to the RAG app and get response
        
        Args:
            query: The question to ask
            user_id: User identifier for context
            
        Returns:
            dict with keys: query, context, answer
            
        Raises:
            httpx.HTTPError: If request fails
            TimeoutError: If request times out
        """
        try:
            endpoint = f"{self.base_url}/ask"
            params = {
                "query": query,
                "user_id": user_id
            }
            
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(endpoint, params=params)
                response.raise_for_status()
                
                data = response.json()
                return data
                
        except httpx.TimeoutException as e:
            logger.error(f"RAG app timeout for query: {query}")
            raise TimeoutError(f"RAG app did not respond within {self.timeout}s") from e
            
        except httpx.HTTPStatusError as e:
            logger.error(f"RAG app error for query: {query}, status: {e.response.status_code}")
            raise
            
        except Exception as e:
            logger.error(f"Error communicating with RAG app: {str(e)}")
            raise

    async def history(self, user_id: str, limit: Optional[int] = None) -> dict:
        """
        Fetch query history from the RAG app.

        Args:
            user_id: User identifier
            limit: Optional number of records

        Returns:
            dict with keys: user_id, count, history
        """
        try:
            endpoint = f"{self.base_url}/history"
            params = {"user_id": user_id}
            if limit is not None:
                params["limit"] = limit

            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(endpoint, params=params)
                response.raise_for_status()
                return response.json()

        except httpx.TimeoutException as e:
            logger.error(f"RAG history timeout for user_id: {user_id}")
            raise TimeoutError(f"RAG history did not respond within {self.timeout}s") from e

        except httpx.HTTPStatusError as e:
            logger.error(
                f"RAG history error for user_id: {user_id}, status: {e.response.status_code}"
            )
            raise

        except Exception as e:
            logger.error(f"Error fetching RAG history: {str(e)}")
            raise


# Global instance
rag_client = RAGClient()
