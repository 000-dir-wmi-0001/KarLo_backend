"""RAG API routes"""
from fastapi import APIRouter, HTTPException, Query, Request, status
from app.karlo_c.schemas import rag_schema
from app.karlo_c.services.rag import rag_service


rag_router = APIRouter(prefix="/rag", tags=["RAG"])


def _get_auth_user_id(request: Request) -> str:
    """Extract user ID from JWT token"""
    token_payload = getattr(request.state, "user", None)
    token_sub = token_payload.get("sub") if isinstance(token_payload, dict) else None
    if token_sub is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    return str(token_sub)


@rag_router.post("/ask", response_model=rag_schema.RAGAskResponse, status_code=status.HTTP_200_OK)
async def ask_rag(
    query_request: rag_schema.RAGQueryRequest,
    request: Request
):
    """
    Ask a question to the RAG system
    
    - **query**: The question to ask (1-1000 characters)
    
    Returns the query, relevant context, and answer from RAG app
    """
    try:
        user_id = _get_auth_user_id(request)
        
        # Call RAG service
        response = await rag_service.ask_question(query_request.query, user_id)
        
        return {
            "data": response,
            "message": "Query answered successfully"
        }
        
    except TimeoutError as e:
        raise HTTPException(
            status_code=status.HTTP_504_GATEWAY_TIMEOUT,
            detail="RAG service did not respond in time. Please try again."
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Error communicating with RAG service: {str(e)}"
        )


@rag_router.get("/history", response_model=rag_schema.RAGHistoryApiResponse, status_code=status.HTTP_200_OK)
async def get_rag_history(
    request: Request,
    limit: int = Query(default=20, ge=1, le=100),
):
    """
    Get authenticated user's RAG history.

    - **limit**: Optional number of history items (1-100)
    """
    try:
        user_id = _get_auth_user_id(request)
        response = await rag_service.get_history(user_id=user_id, limit=limit)
        return {
            "data": response,
            "message": "History fetched successfully",
        }

    except TimeoutError:
        raise HTTPException(
            status_code=status.HTTP_504_GATEWAY_TIMEOUT,
            detail="RAG history service did not respond in time. Please try again.",
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Error communicating with RAG history service: {str(e)}",
        )
