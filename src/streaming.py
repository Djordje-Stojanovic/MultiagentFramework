"""
Multi-model streaming functionality for agent conversations
Keeps main file under 200 LOC limit per Elon's efficiency algorithm
"""

from fastapi import WebSocket, WebSocketDisconnect
import json
from pydantic_ai import Agent


async def handle_websocket_stream(websocket: WebSocket, agents: dict):
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
            
            if not content.strip():
                await websocket.send_text(json.dumps({
                    "type": "error", 
                    "content": "Please provide content!"
                }))
                continue
            
            # Update conversation history from client if provided
            if history:
                conversation_history = history
            
            if message_type == "prompt":
                # Single agent streaming with conversation context
                primary_agent = agents['primary']
                agent_name = "primary"
                
                await websocket.send_text(json.dumps({
                    "type": "agent_start", 
                    "agent": agent_name
                }))
                
                # Build context-aware prompt
                if conversation_history:
                    context_prompt = f"""Conversation history:
{chr(10).join([f"{msg['role']}: {msg['content']}" for msg in conversation_history[-10:]])}

User: {content}"""
                else:
                    context_prompt = content
                
                async with primary_agent.run_stream(context_prompt) as result:
                    agent_response = ""
                    async for chunk in result.stream_text(delta=True, debounce_by=None):
                        agent_response += chunk
                        await websocket.send_text(json.dumps({
                            "type": "token", 
                            "content": chunk,
                            "agent": agent_name
                        }))
                    
                    conversation_history.append({"role": "User", "content": content})
                    conversation_history.append({"role": "Agent", "content": agent_response})
                
                await websocket.send_text(json.dumps({
                    "type": "agent_end", 
                    "agent": agent_name
                }))
            
            elif message_type == "debate":
                # Multi-agent streaming debate
                first_agent = agents['first'] 
                second_agent = agents['second']
                responses = {}
                
                # First agent initiates
                await websocket.send_text(json.dumps({
                    "type": "agent_start", 
                    "agent": "first"
                }))
                
                async with first_agent.run_stream(f"Start a discussion about: {content}") as result:
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
                
                async with second_agent.run_stream(f"Respond to: {responses['first']}") as result:
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
                
                async with first_agent.run_stream(f"Final reply to: {responses['second']}") as result:
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
                
    except WebSocketDisconnect:
        pass
    except Exception as e:
        await websocket.send_text(json.dumps({
            "type": "error", 
            "content": f"Error: {str(e)}"
        }))
