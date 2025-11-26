from fastapi import APIRouter, HTTPException
from services.redis_service import redis_service
from core.logger import logger

router = APIRouter()

@router.get("/session/{session_id}")
async def get_session(session_id: str):
    """
    Retrieve session data by session ID.
    
    Args:
        session_id (str): The session ID
        
    Returns:
        dict: Session data
    """
    try:
        logger.info(f"Retrieving session data for ID: {session_id}")
        session_data = redis_service.get_session(session_id)
        
        if session_data:
            return {
                "status": True,
                "data": session_data
            }
        else:
            raise HTTPException(status_code=404, detail="Session not found")
            
    except Exception as e:
        logger.error(f"Error retrieving session {session_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to retrieve session: {str(e)}")


@router.delete("/session/{session_id}")
async def delete_session(session_id: str):
    """
    Delete a session by session ID.
    
    Args:
        session_id (str): The session ID
        
    Returns:
        dict: Deletion status
    """
    try:
        logger.info(f"Deleting session with ID: {session_id}")
        result = redis_service.delete_session(session_id)
        
        if result:
            return {
                "status": True,
                "message": "Session deleted successfully"
            }
        else:
            raise HTTPException(status_code=404, detail="Session not found")
            
    except Exception as e:
        logger.error(f"Error deleting session {session_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to delete session: {str(e)}")