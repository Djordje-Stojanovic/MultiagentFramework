#!/usr/bin/env python3
"""
MultiAgent Framework - Main Application
Minimal FastAPI app with streaming agents (under 200 LOC per Elon's algorithm)
"""

import os
from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
from pydantic_ai import Agent
from dotenv import load_dotenv
from streaming import handle_websocket_stream
from ui import get_html_interface

# Load environment
load_dotenv()

app = FastAPI(title="MultiAgent Framework")

# Initialize agents - generic configuration
AGENTS = {
    'primary': Agent(
        'gemini-2.0-flash-exp',
        system_prompt="You are a helpful AI assistant engaging in natural conversation.",
    ),
    'first': Agent(
        'gemini-2.0-flash-exp', 
        system_prompt="You start discussions thoughtfully and present initial viewpoints.",
    ),
    'second': Agent(
        'gemini-2.0-flash-exp',
        system_prompt="You provide thoughtful counter-arguments and alternative perspectives.",
    )
}

@app.get("/", response_class=HTMLResponse)
async def root():
    """Main interface - dark mode only"""
    return get_html_interface()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for streaming"""
    await handle_websocket_stream(websocket, AGENTS)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
