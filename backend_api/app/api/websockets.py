import json
from typing import Dict
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Query
from pydantic import ValidationError

from app.schemas.ai_contract import AIRequestPayload, AIResponsePayload
from app.core.security import verify_ws_token

router = APIRouter()

class ConnectionManager:
    """
    Manages active WebSocket connections so we can route AI events to the correct user/session.
    """
    def __init__(self):
        # Maps session_id to the active WebSocket connection
        self.active_connections: Dict[str, WebSocket] = {}

    async def connect(self, websocket: WebSocket, session_id: str):
        await websocket.accept()
        self.active_connections[session_id] = websocket

    def disconnect(self, session_id: str):
        if session_id in self.active_connections:
            del self.active_connections[session_id]

    async def send_personal_message(self, message: str, session_id: str):
        """Send a serialized string payload to a specific session."""
        if session_id in self.active_connections:
            await self.active_connections[session_id].send_text(message)

manager = ConnectionManager()

@router.websocket("/ws/{session_id}")
async def websocket_endpoint(websocket: WebSocket, session_id: str, token: str = Query(...)):
    """
    The main persistent pipeline.
    The 'token' is required in the URL (e.g., /ws/123?token=jwt_here) to secure the socket.
    """
    # 1. SECURITY CHECK: Verify the JWT token before accepting the connection!
    user_id = verify_ws_token(token)
    
    await manager.connect(websocket, session_id)
    try:
        while True:
            # Wait for data from the Next.js frontend
            data = await websocket.receive_text()
            
            try:
                # 1. Unpack the Envelope and Validate against our Contract
                payload_dict = json.loads(data)
                request_payload = AIRequestPayload(**payload_dict)
                
                # 2. (Future) We will pass request_payload to your partner's ai_core here!
                
                # 3. For now, we mock a response back matching the AIResponsePayload contract
                mock_response = AIResponsePayload(
                    event_type="agent_status",
                    agent_name="system",
                    data={"status": f"Platform received your action: '{request_payload.action}'"}
                )
                
                # Send the validated JSON back down the pipe
                await manager.send_personal_message(mock_response.model_dump_json(), session_id)
                
            except ValidationError as e:
                # The frontend sent something that broke the contract
                error_resp = {"event_type": "error", "data": {"message": "Invalid contract payload", "details": e.errors()}}
                await manager.send_personal_message(json.dumps(error_resp), session_id)
            except json.JSONDecodeError:
                # The frontend sent malformed JSON
                error_resp = {"event_type": "error", "data": {"message": "Invalid JSON string received"}}
                await manager.send_personal_message(json.dumps(error_resp), session_id)
                
    except WebSocketDisconnect:
        manager.disconnect(session_id)
