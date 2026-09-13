from fastapi import FastAPI
from prometheus_client import make_asgi_app
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

from app.api.websockets import router as websocket_router

app = FastAPI(
    title="Adaptive Multi-Agent Platform",
    description="Backend API and WebSocket control plane for the AI system.",
    version="0.1.0"
)

# 1. Mount Prometheus Metrics endpoint
metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)

# 2. Auto-instrument FastAPI with OpenTelemetry
FastAPIInstrumentor.instrument_app(app)

# Include our modular WebSocket router
app.include_router(websocket_router)

@app.get("/health")
def health_check():
    """
    Standard REST endpoint for Kubernetes/Docker health probes.
    """
    return {"status": "ok", "message": "Control plane is running."}
