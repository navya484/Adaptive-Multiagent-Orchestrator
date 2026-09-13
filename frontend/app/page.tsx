import AgentChat from "./components/AgentChat";

export default function Home() {
  return (
    <main className="min-h-screen bg-black flex flex-col items-center justify-center p-8">
      <div className="text-center mb-8">
        <h1 className="text-4xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-purple-600 tracking-tight">
          Adaptive Multi-Agent Platform
        </h1>
        <p className="mt-2 text-gray-400">Control Plane & Observability Dashboard</p>
      </div>
      
      <div className="w-full max-w-4xl">
        <AgentChat />
      </div>
    </main>
  );
}
