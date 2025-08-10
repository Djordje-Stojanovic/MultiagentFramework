"""
Multi-model streaming functionality for agent conversations
Keeps main file under 200 LOC limit per Elon's efficiency algorithm
"""

from fastapi import WebSocket, WebSocketDisconnect
import json
from pydantic_ai import Agent, RunContext
from pydantic_ai.settings import ModelSettings
from dataclasses import dataclass
from typing import List


@dataclass
class Deps:
    system_prompt: str


async def handle_websocket_stream(websocket: WebSocket, create_agent_func):
    """Multi-model streaming handler - works with any Pydantic AI model"""
    await websocket.accept()
    
    # Store conversation history per WebSocket connection
    conversation_history = []
    
    try:
        while True:
            # Receive message from client
            data = await websocket.receive_text()
            message = json.loads(data)
            
            message_type = message.get("type", "prompt")
            content = message.get("content", "")
            history = message.get("history", [])
            config = message.get("config", {})
            
            if not content.strip():
                await websocket.send_text(json.dumps({
                    "type": "error", 
                    "content": "Please provide content!"
                }))
                continue
            
            # Extract config parameters with defaults
            model = config.get("model", "gemini-2.5-flash")
            temperature = config.get("temperature", 0.7)
            top_p = config.get("top_p", 0.9)
            top_k = config.get("top_k", 40)
            max_tokens = config.get("max_tokens", 1024)
            system_prompt = config.get("system_prompt", "").strip()
            
            # Prepare system prompt for dynamic injection
            if system_prompt:
                base_prompt = "You are a helpful AI assistant."
                effective_prompt = f"{base_prompt}\n\n{system_prompt}".strip()
            else:
                effective_prompt = "You are a helpful AI assistant."
            
            if message_type == "prompt":
                # Single agent streaming with proper message history
                primary_agent = create_agent_func(model=model)  # No hardcoded system_prompt
                agent_name = "primary"
                
                # Create ModelSettings with user configuration (top_k not available in Pydantic AI)
                model_settings = ModelSettings(
                    temperature=temperature,
                    top_p=top_p,
                    max_tokens=max_tokens
                )
                
                await websocket.send_text(json.dumps({
                    "type": "agent_start", 
                    "agent": agent_name
                }))
                
                # Use dynamic system prompt via deps
                deps = Deps(system_prompt=effective_prompt)
                async with primary_agent.run_stream(
                    content, 
                    model_settings=model_settings,
                    deps=deps,
                    message_history=[]  # Start fresh for now
                ) as result:
                    agent_response = ""
                    async for chunk in result.stream_text(delta=True, debounce_by=None):
                        agent_response += chunk
                        await websocket.send_text(json.dumps({
                            "type": "token", 
                            "content": chunk,
                            "agent": agent_name
                        }))
                    
                    # Store conversation history
                    conversation_history.append({"role": "User", "content": content})
                    conversation_history.append({"role": "Agent", "content": agent_response})
                
                await websocket.send_text(json.dumps({
                    "type": "agent_end", 
                    "agent": agent_name
                }))
            
            elif message_type == "debate":
                # Multi-agent streaming debate
                first_agent = create_agent_func(
                    model=model,
                    system_prompt="You start discussions thoughtfully and present initial viewpoints."
                )
                second_agent = create_agent_func(
                    model=model,
                    system_prompt="You provide thoughtful counter-arguments and alternative perspectives."
                )
                
                # Create ModelSettings with user configuration (top_k not available in Pydantic AI)
                model_settings = ModelSettings(
                    temperature=temperature,
                    top_p=top_p,
                    max_tokens=max_tokens
                )
                
                responses = {}
                
                # First agent initiates
                await websocket.send_text(json.dumps({
                    "type": "agent_start", 
                    "agent": "first"
                }))
                
                async with first_agent.run_stream(f"Start a discussion about: {content}", model_settings=model_settings) as result:
                    responses['first'] = ""
                    async for chunk in result.stream_text(delta=True, debounce_by=None):
                        responses['first'] += chunk
                        await websocket.send_text(json.dumps({
                            "type": "token", 
                            "content": chunk,
                            "agent": "first"
                        }))
                
                await websocket.send_text(json.dumps({
                    "type": "agent_end", 
                    "agent": "first"
                }))
                
                # Second agent responds
                await websocket.send_text(json.dumps({
                    "type": "agent_start", 
                    "agent": "second"
                }))
                
                async with second_agent.run_stream(f"Respond to: {responses['first']}", model_settings=model_settings) as result:
                    responses['second'] = ""
                    async for chunk in result.stream_text(delta=True, debounce_by=None):
                        responses['second'] += chunk
                        await websocket.send_text(json.dumps({
                            "type": "token", 
                            "content": chunk,
                            "agent": "second"
                        }))
                
                await websocket.send_text(json.dumps({
                    "type": "agent_end", 
                    "agent": "second"
                }))
                
                # First agent final reply
                await websocket.send_text(json.dumps({
                    "type": "agent_start", 
                    "agent": "first"
                }))
                
                async with first_agent.run_stream(f"Final reply to: {responses['second']}", model_settings=model_settings) as result:
                    async for chunk in result.stream_text(delta=True, debounce_by=None):
                        await websocket.send_text(json.dumps({
                            "type": "token", 
                            "content": chunk,
                            "agent": "first"
                        }))
                
                await websocket.send_text(json.dumps({
                    "type": "agent_end", 
                    "agent": "first"
                }))
            
            await websocket.send_text(json.dumps({
                "type": "complete"
            }))
                
    except WebSocketDisconnect as e:
        # Log close codes to distinguish normal vs problematic disconnections
        # 1000/1001 = normal closures, 1006/1002/1011 = problematic
        print(f"WebSocket closed with code: {e.code} ({'normal' if e.code in [1000, 1001] else 'abnormal'})")
    except Exception as e:
        print(f"WebSocket error: {str(e)}")
        try:
            await websocket.send_text(json.dumps({
                "type": "error", 
                "content": f"Error: {str(e)}"
            }))
        except:
            # Connection might be already closed
            pass
