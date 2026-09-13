"use client";

import { useEffect, useState, useRef } from "react";

export default function AgentChat() {
  const [status, setStatus] = useState("Connecting...");
  const [messages, setMessages] = useState<string[]>([]);
  const ws = useRef<WebSocket | null>(null);

  useEffect(() => {
    // For dev purposes, we use a mocked JWT token. In production, this comes from next-auth or similar.
    const mockToken = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0ZXN0X3VzZXJfMTIzIn0.X-a-Y_h_something_mocked";
    const session_id = "session-" + Math.random().toString(36).substring(7);
    
    // Connect to FastAPI WebSocket backend with the token in the URL
    ws.current = new WebSocket(`ws://localhost:8000/ws/${session_id}?token=${mockToken}`);

    ws.current.onopen = () => setStatus("Connected to Platform");
    
    ws.current.onmessage = (event) => {
      // Expecting JSON based on our AIResponsePayload Contract
      const response = JSON.parse(event.data);
      setMessages((prev) => [...prev, JSON.stringify(response)]);
    };

    ws.current.onclose = () => setStatus("Disconnected");

    // Cleanup when component unmounts
    return () => {
      ws.current?.close();
    };
  }, []);

  const handleStartTask = () => {
    if (ws.current && ws.current.readyState === WebSocket.OPEN) {
      // Send data matching our AIRequestPayload Contract
      const payload = {
        session_id: "test-session",
        action: "start_task",
        prompt: "Initialize multi-agent orchestrator...",
        context: {}
      };
      ws.current.send(JSON.stringify(payload));
    }
  };

  return (
    <div className="p-6 max-w-lg mx-auto bg-gray-900 text-white rounded-xl shadow-md space-y-4 border border-gray-800">
      <div className="flex items-center space-x-2">
        <div className={`w-3 h-3 rounded-full ${status === "Connected to Platform" ? "bg-green-500" : "bg-red-500"}`}></div>
        <h2 className="text-xl font-bold">Multi-Agent Control</h2>
      </div>
      <p className="text-sm text-gray-400">Status: {status}</p>
      
      <button 
        onClick={handleStartTask}
        className="px-4 py-2 bg-blue-600 hover:bg-blue-700 rounded-md font-semibold transition-colors"
      >
        Trigger AI Core
      </button>

      <div className="mt-4 p-3 bg-black rounded h-48 overflow-y-auto font-mono text-sm">
        {messages.map((msg, idx) => (
          <div key={idx} className="mb-2 text-green-400 border-b border-gray-800 pb-1">
            {msg}
          </div>
        ))}
        {messages.length === 0 && <span className="text-gray-600">Awaiting stream...</span>}
      </div>
    </div>
  );
}
