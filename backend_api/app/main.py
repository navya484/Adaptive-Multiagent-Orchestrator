from fastapi import FastAPI
from app.api.websockets import router as websocket_router

app = FastAPI(
    title="Adaptive Multi-Agent Platform",
    description="Backend API and WebSocket control plane for the AI system.",
    version="0.1.0"
)

# Include our modular WebSocket router
app.include_router(websocket_router)

@app.get("/health")
def health_check():
    """
    Standard REST endpoint for Kubernetes/Docker health probes.
    """
    return {"status": "ok", "message": "Control plane is running."}
