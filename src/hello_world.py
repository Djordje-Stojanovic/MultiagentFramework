#!/usr/bin/env python3
"""
MultiAgent Framework - Main Application
Minimal FastAPI app with streaming agents (under 200 LOC per Elon's algorithm)
"""

import os
from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
from pydantic_ai import Agent
from pydantic_ai.settings import ModelSettings
from dotenv import load_dotenv
from streaming import handle_websocket_stream
from ui import get_html_interface

# Load environment
load_dotenv()

app = FastAPI(title="MultiAgent Framework")

def create_agent(model: str, system_prompt: str = None) -> Agent:
    """Create a dynamically configured agent (ModelSettings applied per-request)"""
    from streaming import Deps
    
    if system_prompt:
        return Agent(model, system_prompt=system_prompt)
    else:
        # Create agent with dynamic system prompt support
        agent = Agent(model, deps_type=Deps)
        
        @agent.system_prompt
        def dynamic_system_prompt(ctx) -> str:
            return ctx.deps.system_prompt
        
        return agent

@app.get("/", response_class=HTMLResponse)
async def root():
    """Main interface - dark mode only"""
    return get_html_interface()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for streaming"""
    await handle_websocket_stream(websocket, create_agent)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
