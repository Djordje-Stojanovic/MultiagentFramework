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

# Initialize Pydantic AI agent with Gemini
agent = Agent(
    model=GeminiModel('gemini-2.0-flash-exp'),  # Using Flash for simple tasks
    system_prompt="You are a helpful assistant. Keep responses brief and friendly."
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
        <h1>🤖 MultiAgent Framework - Hello World</h1>
        <p>Click the button to test Pydantic AI integration:</p>
        <button onclick="testAgent()">Say Hello!</button>
        <div id="response" class="response" style="display:none;"></div>
        
        <script>
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
        </script>
    </body>
    </html>
    """

@app.get("/hello")
async def hello():
    """Test endpoint for our agent"""
    try:
        result = await agent.run("Give me a one-line greeting!")
        # Extract the output from the AgentRunResult
        return {"message": result.output}
    except Exception as e:
        return {"message": f"Error: {str(e)}"}

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
