from pydantic import BaseModel, Field
from typing import Dict, Any, Optional, Literal


class AIRequestPayload(BaseModel):
    """
    The payload sent from the Platform to the AI Core.
    """
    session_id: str = Field(..., description="Unique ID for the session")
    action: Literal["start_task", "provide_feedback", "abort"] = Field(..., description="Action to perform")
    prompt: Optional[str] = Field(None, description="The user's input prompt")
    context: Dict[str, Any] = Field(default_factory=dict, description="Additional context or history")


class AIResponsePayload(BaseModel):
    """
    The payload yielded/returned by the AI Core back to the Platform.
    """
    event_type: Literal["token_chunk", "agent_status", "task_complete", "error"] = Field(
        ..., description="The type of event being emitted"
    )
    agent_name: Optional[str] = Field(None, description="Which agent in the multi-agent system is reporting")
    data: Dict[str, Any] = Field(
        ..., description="The actual content (e.g., {'chunk': ' Hello'}, or {'status': 'searching_db'})"
    )
