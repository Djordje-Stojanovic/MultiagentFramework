"""
Hello World with Pydantic AI and FastAPI
Simple proof of concept to verify our tech stack
"""

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic_ai import Agent
from pydantic_ai.models.gemini import GeminiModel
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize FastAPI
app = FastAPI(title="MultiAgent Framework - Hello World")

# Initialize Pydantic AI agents with Gemini
agent1 = Agent(
    model=GeminiModel('gemini-2.0-flash-exp'),
    system_prompt="You are Agent 1. Your job is to initiate a discussion with Agent 2 based on the user's topic."
)

agent2 = Agent(
    model=GeminiModel('gemini-2.0-flash-exp'),
    system_prompt="You are Agent 2. Your job is to respond to Agent 1's discussion point with a counter-argument or a different perspective."
)

@app.get("/", response_class=HTMLResponse)
async def home():
    """Simple HTML interface"""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>MultiAgent Framework - Hello World</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                max-width: 800px;
                margin: 50px auto;
                padding: 20px;
                background: #f5f5f5;
            }
            h1 { color: #333; }
            .response {
                background: white;
                padding: 15px;
                border-radius: 8px;
                margin-top: 20px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }
            button {
                background: #4CAF50;
                color: white;
                padding: 10px 20px;
                border: none;
                border-radius: 4px;
                cursor: pointer;
                font-size: 16px;
            }
            button:hover { background: #45a049; }
        </style>
    </head>
    <body>
        <h1>🤖 MultiAgent Framework - Enhanced UI</h1>
        
        <!-- Model Configuration Settings -->
        <div class="response">
            <h3>🔧 Current Model Configuration</h3>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-top: 10px;">
                <div><strong>Model:</strong> gemini-2.0-flash-exp</div>
                <div><strong>Provider:</strong> Google Gemini API</div>
                <div><strong>Temperature:</strong> 0.7 (default - controls randomness)</div>
                <div><strong>Top-P:</strong> 0.95 (default - nucleus sampling)</div>
                <div><strong>Top-K:</strong> 40 (default - top-k sampling)</div>
                <div><strong>Max Tokens:</strong> 8192 (default output limit)</div>
            </div>
            <div style="margin-top: 15px;">
                <h4>🤖 Agent Roles:</h4>
                <div style="background: #f0f8ff; padding: 10px; margin: 5px 0; border-radius: 4px;">
                    <strong>Agent 1:</strong> "You are Agent 1. Your job is to initiate a discussion with Agent 2 based on the user's topic."
                </div>
                <div style="background: #f0fff0; padding: 10px; margin: 5px 0; border-radius: 4px;">
                    <strong>Agent 2:</strong> "You are Agent 2. Your job is to respond to Agent 1's discussion point with a counter-argument or a different perspective."
                </div>
            </div>
            <div style="margin-top: 10px; font-size: 12px; color: #666;">
                <strong>Available Parameters:</strong> temperature (0-2), topP (0-1), topK (1-40), max_output_tokens, stop_sequences, system_instruction
            </div>
        </div>
        
        <!-- Custom Prompt Interface -->
        <div style="margin: 20px 0;">
            <textarea id="promptInput" placeholder="Enter your custom prompt here..." 
                style="width: 100%; height: 80px; padding: 10px; border: 1px solid #ddd; border-radius: 4px;"></textarea>
            <button onclick="sendCustomPrompt()" style="margin-top: 10px;">Send Custom Prompt</button>
            <button onclick="testAgent()" style="margin-left: 10px;">Quick Test</button>
        </div>
        
        <div id="response" class="response" style="display:none;"></div>

        <!-- Two-Agent Conversation -->
        <div style="margin: 40px 0;">
            <h2>Two-Agent Conversation</h2>
            <input type="text" id="topicInput" placeholder="Enter a topic for the agents to discuss..." style="width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 4px;">
            <button onclick="startDebate()" style="margin-top: 10px;">Start Debate</button>
            <div id="debateResponse" class="response" style="display:none; margin-top: 20px;"></div>
        </div>
        
        <script>
            async function startDebate() {
                const topicInput = document.getElementById('topicInput');
                const topic = topicInput.value.trim();

                if (!topic) {
                    alert('Please enter a topic for the debate!');
                    return;
                }

                const debateResponseDiv = document.getElementById('debateResponse');
                debateResponseDiv.style.display = 'block';
                debateResponseDiv.innerHTML = 'Agents are discussing...';

                try {
                    const response = await fetch('/debate', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ topic: topic })
                    });

                    const data = await response.json();
                    let html = `<strong>Topic:</strong> "${topic}"<br><br>`;
                    html += `<strong>Agent 1:</strong> ${data.agent1_initial_statement}<br><br>`;
                    html += `<strong>Agent 2:</strong> ${data.agent2_response}<br><br>`;
                    html += `<strong>Agent 1 Final Reply:</strong> ${data.agent1_final_reply}`;
                    debateResponseDiv.innerHTML = html;
                } catch (error) {
                    debateResponseDiv.innerHTML = `<strong>Error:</strong> ${error.message}`;
                }
            }

            async function testAgent() {
                const responseDiv = document.getElementById('response');
                responseDiv.style.display = 'block';
                responseDiv.innerHTML = 'Loading...';
                
                try {
                    const response = await fetch('/hello');
                    const data = await response.json();
                    responseDiv.innerHTML = `<strong>Agent says:</strong> ${data.message}`;
                } catch (error) {
                    responseDiv.innerHTML = `<strong>Error:</strong> ${error.message}`;
                }
            }
            
            async function sendCustomPrompt() {
                const promptInput = document.getElementById('promptInput');
                const prompt = promptInput.value.trim();
                
                if (!prompt) {
                    alert('Please enter a prompt first!');
                    return;
                }
                
                const responseDiv = document.getElementById('response');
                responseDiv.style.display = 'block';
                responseDiv.innerHTML = 'Processing your prompt...';
                
                try {
                    const response = await fetch('/prompt', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({prompt: prompt})
                    });
                    
                    const data = await response.json();
                    responseDiv.innerHTML = `<strong>Your prompt:</strong> "${prompt}"<br><br><strong>Agent response:</strong> ${data.message}`;
                } catch (error) {
                    responseDiv.innerHTML = `<strong>Error:</strong> ${error.message}`;
                }
            }
        </script>
    </body>
    </html>
    """

@app.get("/hello")
async def hello():
    """Test endpoint for our agent"""
    try:
        result = await agent1.run("Give me a one-line greeting!")
        # Extract the output from the AgentRunResult
        return {"message": result.output}
    except Exception as e:
        return {"message": f"Error: {str(e)}"}

@app.post("/prompt")
async def custom_prompt(prompt_data: dict):
    """Endpoint for custom prompts"""
    try:
        user_prompt = prompt_data.get("prompt", "")
        if not user_prompt.strip():
            return {"message": "Please provide a prompt!"}
        
        result = await agent1.run(user_prompt)
        return {"message": result.output}
    except Exception as e:
        return {"message": f"Error: {str(e)}"}

@app.post("/debate")
async def debate(prompt_data: dict):
    """Endpoint for two-agent debate"""
    try:
        topic = prompt_data.get("topic", "")
        if not topic.strip():
            return {"message": "Please provide a topic!"}

        # Agent 1 initiates
        agent1_statement = await agent1.run(f"Start a discussion about: {topic}")
        
        # Agent 2 responds
        agent2_response = await agent2.run(f"Respond to this statement: {agent1_statement.output}")

        # Agent 1 gives final reply
        agent1_final_reply = await agent1.run(f"Give a final reply to this response: {agent2_response.output}")

        return {
            "agent1_initial_statement": agent1_statement.output,
            "agent2_response": agent2_response.output,
            "agent1_final_reply": agent1_final_reply.output
        }
    except Exception as e:
        return {"message": f"Error: {str(e)}"}

@app.get("/model-info")
async def model_info():
    """Get current model information"""
    return {
        "model": "gemini-2.0-flash-exp",
        "provider": "Google Gemini",
        "system_prompt": "You are a helpful assistant. Keep responses brief and friendly.",
        "framework": "Pydantic AI"
    }

@app.get("/health")
async def health():
    """Health check endpoint"""
    return {"status": "healthy", "framework": "Pydantic AI + FastAPI"}

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting MultiAgent Framework - Hello World")
    print("📍 Open http://localhost:8000 in your browser")
    print("🔄 Auto-reload enabled - server will restart on file changes")
    uvicorn.run("hello_world:app", host="0.0.0.0", port=8000, reload=True)
