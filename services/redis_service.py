import os
import json
import uuid
from typing import Dict, Any, Optional
from datetime import datetime

import redis
from core.logger import logger


class RedisService:
    """Service for managing sessions stored in Redis."""

    def __init__(self):
        self.host = os.getenv("REDIS_HOST", "localhost")
        self.port = int(os.getenv("REDIS_PORT", 6379))
        self.db = int(os.getenv("REDIS_DB", 0))
        self.enabled = os.getenv("REDIS_ENABLED", "true").lower() == "true"

        self.client = None

        if not self.enabled:
            logger.info("Redis is disabled via environment variable.")
            return

        try:
            self.client = redis.Redis(
                host=self.host,
                port=self.port,
                db=self.db,
                decode_responses=True,
            )
            self.client.ping()
            logger.info(f"Connected to Redis at {self.host}:{self.port}")
        except Exception as e:
            logger.warning(
                f"Redis connection failed: {e}. Redis features will be disabled."
            )
            self.client = None

    # ----------------------------------------------------------------------
    def _generate_session_id(self) -> str:
        """Always return a real UUID for session id."""
        return str(uuid.uuid4())

    def _current_timestamp(self) -> str:
        """Return an ISO formatted UTC timestamp."""
        return datetime.utcnow().isoformat()

    def _dummy_session_data(self, session_id: str) -> Dict[str, Any]:
        """Return dummy session data when Redis is unavailable."""
        return {
            "session_id": session_id,
            "parsed_data": {},
            "created_at": self._current_timestamp(),
        }

    # ----------------------------------------------------------------------
    def create_session(self, parsed_data: Dict[Any, Any]) -> str:
        """Create a new session and store it in Redis."""

        session_id = self._generate_session_id()  # Always generate real ID

        print(self.client)

        if not self.client:
            logger.warning("Redis not available. Returning real session ID (dummy mode).")
            return session_id

        try:
            session_data = {
                "session_id": session_id,
                "parsed_data": parsed_data,
                "created_at": self._current_timestamp(),
            }

            session_json = json.dumps(session_data)

            # TTL: 24 hours
            self.client.setex(f"session:{session_id}", 86400, session_json)

            logger.info(f"Session created: {session_id}")
            return session_id

        except Exception as e:
            logger.error(f"Error creating session: {e}")
            raise Exception(f"Session creation failed: {e}")

    # ----------------------------------------------------------------------
    def get_session(self, session_id: str) -> Optional[Dict[Any, Any]]:
        """Retrieve a session from Redis."""

        if not self.client:
            logger.warning("Redis not available. Returning dummy session data.")
            return self._dummy_session_data(session_id)

        try:
            session_json = self.client.get(f"session:{session_id}")

            if not session_json:
                logger.warning(f"Session not found: {session_id}")
                return None

            session_data = json.loads(session_json)
            logger.info(f"Session retrieved: {session_id}")
            return session_data

        except Exception as e:
            logger.error(f"Error retrieving session {session_id}: {e}")
            raise Exception(f"Session retrieval failed: {e}")

    # ----------------------------------------------------------------------
    def delete_session(self, session_id: str) -> bool:
        """Delete a session from Redis."""

        if not self.client:
            logger.warning("Redis not available. Skipping deletion.")
            return True

        try:
            result = self.client.delete(f"session:{session_id}")

            if result:
                logger.info(f"Session deleted: {session_id}")
                return True

            logger.warning(f"Session not found for deletion: {session_id}")
            return False

        except Exception as e:
            logger.error(f"Error deleting session {session_id}: {e}")
            raise Exception(f"Session deletion failed: {e}")


# Singleton instance
redis_service = RedisService()
