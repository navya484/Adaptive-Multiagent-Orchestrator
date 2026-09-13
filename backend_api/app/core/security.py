import jwt
from fastapi import WebSocketException, status

SECRET_KEY = "super-secret-key-change-in-production"
ALGORITHM = "HS256"

def verify_ws_token(token: str) -> str:
    """
    Verifies a JWT token for WebSocket connections.
    Returns the user_id if valid, raises WebSocketException if invalid.
    """
    if not token:
        raise WebSocketException(code=status.WS_1008_POLICY_VIOLATION, reason="Missing authentication token")
    
    try:
        # We expect a payload like: {"sub": "user_123"}
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
            raise WebSocketException(code=status.WS_1008_POLICY_VIOLATION, reason="Invalid token payload")
        return user_id
    except jwt.PyJWTError:
        raise WebSocketException(code=status.WS_1008_POLICY_VIOLATION, reason="Invalid authentication token")

def create_mock_token(user_id: str = "test_user_123") -> str:
    """Helper to generate a valid token for our Next.js frontend to use during dev."""
    return jwt.encode({"sub": user_id}, SECRET_KEY, algorithm=ALGORITHM)
