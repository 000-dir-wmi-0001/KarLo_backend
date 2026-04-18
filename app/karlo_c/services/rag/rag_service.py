"""RAG service - handles RAG app communication and business logic"""
from app.karlo_c.services.rag.rag_client import rag_client
from app.karlo_c.schemas.rag_schema import RAGHistoryResponse, RAGQueryResponse
import logging

logger = logging.getLogger(__name__)


class RAGService:
    """Service for handling RAG queries"""
    
    @staticmethod
    async def ask_question(query: str, user_id: str) -> RAGQueryResponse:
        """
        Ask a question to the RAG app
        
        Args:
            query: The question to ask
            user_id: User identifier
            
        Returns:
            RAGQueryResponse with query, context, and answer
            
        Raises:
            Exception: If RAG app communication fails
        """
        try:
            # Call RAG app
            rag_response = await rag_client.ask(query, user_id)
            
            # Parse and validate response
            response = RAGQueryResponse(
                query=rag_response.get("query", query),
                context=rag_response.get("context", []),
                answer=rag_response.get("answer", "")
            )
            
            logger.info(f"Successfully answered query for user {user_id}: {query[:50]}...")
            return response
            
        except Exception as e:
            logger.error(f"Error in RAG service for user {user_id}: {str(e)}")
            raise

    @staticmethod
    async def get_history(user_id: str, limit: int | None = None) -> RAGHistoryResponse:
        """Fetch history for a user from the RAG app."""
        try:
            rag_response = await rag_client.history(user_id=user_id, limit=limit)

            history_items = rag_response.get("history", [])
            response = RAGHistoryResponse(
                user_id=str(rag_response.get("user_id", user_id)),
                count=int(rag_response.get("count", len(history_items))),
                history=history_items,
            )

            logger.info(
                f"Successfully fetched RAG history for user {user_id}, count={response.count}"
            )
            return response

        except Exception as e:
            logger.error(f"Error fetching RAG history for user {user_id}: {str(e)}")
            raise


rag_service = RAGService()
