"""
UI Components for MultiAgent Framework
Separated per Elon's algorithm to keep files under 200 LOC
"""

from styles import get_css

def get_html_interface():
    """Returns the complete HTML interface"""
    return """
<!DOCTYPE html>
<html>
<head>
    <title>MultiAgent Framework</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
""" + get_css() + """
    </style>
</head>
<body>
    <div class="container">
        <h1>MultiAgent Framework</h1>
        
        <div class="mode-selector">
            <button id="chatMode" class="active" onclick="setMode('chat')">Chat Mode</button>
            <button id="debateMode" onclick="setMode('debate')">Debate Mode</button>
            <button onclick="clearChat()">Clear</button>
        </div>
        
        <div class="config-panel">
            <h3>Model Configuration</h3>
            <div class="config-grid">
                <div class="config-item">
                    <strong>Model:</strong>
                    <select id="modelSelector" onchange="updateModelDisplay()">
                        <option value="gemini-2.0-flash-exp" selected>gemini-2.0-flash-exp</option>
                        <option value="gemini-2.5-pro-max-thinking">gemini-2.5-pro-max-thinking</option>
                        <option value="gemini-2.5-pro">gemini-2.5-pro</option>
                        <option value="gemini-2.5-flash">gemini-2.5-flash</option>
                        <option value="gemini-2.5-flash-lite">gemini-2.5-flash-lite</option>
                    </select>
                </div>
                <div class="config-item">
                    <strong>Provider:</strong> Google Gemini
                </div>
                <div class="config-item">
                    <strong>Framework:</strong> Pydantic AI
                </div>
                <div class="config-item">
                    <strong>Mode:</strong> <span id="currentModeDisplay">Chat</span>
                </div>
            </div>
            
            <div class="params-grid">
                <div class="param-item">
                    <label for="temperature">Temperature: <span id="tempValue">0.7</span></label>
                    <input type="range" id="temperature" min="0" max="1" step="0.1" value="0.7" oninput="updateParamDisplay('temperature', 'tempValue')">
                </div>
                <div class="param-item">
                    <label for="topP">Top-P: <span id="topPValue">0.9</span></label>
                    <input type="range" id="topP" min="0" max="1" step="0.1" value="0.9" oninput="updateParamDisplay('topP', 'topPValue')">
                </div>
                <div class="param-item">
                    <label for="topK">Top-K: <span id="topKValue">40</span></label>
                    <input type="range" id="topK" min="1" max="100" step="1" value="40" oninput="updateParamDisplay('topK', 'topKValue')">
                </div>
                <div class="param-item">
                    <label for="maxTokens">Max Tokens: </label>
                    <input type="number" id="maxTokens" min="1" max="8192" value="1024">
                </div>
            </div>
        </div>
        
        <div class="chat-container" id="chatContainer">
            <div id="welcomeMessage" class="status">
                Welcome! Choose a mode and start chatting. Streaming enabled.
            </div>
        </div>
        
        <div class="input-container">
            <input type="text" id="messageInput" placeholder="Type your message..." 
                   onkeypress="if(event.key==='Enter') sendMessage()">
            <button class="send-btn" onclick="sendMessage()">Send</button>
        </div>
    </div>

    <script>
        let currentMode = 'chat';
        let ws = null;
        let conversationHistory = [];
        let isStreaming = false;
        
        // Initialize WebSocket connection on page load
        function initWebSocket() {
            if (ws && ws.readyState === WebSocket.OPEN) return;
            
            ws = new WebSocket(`ws://localhost:8000/ws`);
            
            ws.onopen = () => {
                console.log('WebSocket connected');
            };
            
            ws.onclose = () => {
                console.log('WebSocket disconnected, attempting to reconnect...');
                setTimeout(initWebSocket, 1000); // Reconnect after 1 second
            };
            
            ws.onerror = (error) => {
                console.error('WebSocket error:', error);
            };
            
            ws.onmessage = handleWebSocketMessage;
        }
        
        function handleWebSocketMessage(event) {
            const data = JSON.parse(event.data);
            const container = document.getElementById('chatContainer');
            
            if (data.type === 'agent_start') {
                currentAgent = data.agent;
                streamContent = '';
                
                // Create unique ID with timestamp to avoid conflicts
                const uniqueId = 'streaming-' + currentAgent + '-' + Date.now();
                currentAgentDiv = document.createElement('div');
                currentAgentDiv.id = uniqueId;
                currentAgentDiv.className = 'agent-response typing';
                currentAgentDiv.innerHTML = `<strong>${currentAgent.charAt(0).toUpperCase() + currentAgent.slice(1)}:</strong> `;
                container.appendChild(currentAgentDiv);
                
            } else if (data.type === 'token') {
                streamContent += data.content;
                if (currentAgentDiv) {
                    currentAgentDiv.innerHTML = `<strong>${currentAgent.charAt(0).toUpperCase() + currentAgent.slice(1)}:</strong> ${streamContent}`;
                }
            } else if (data.type === 'agent_end') {
                if (currentAgentDiv) {
                    currentAgentDiv.classList.remove('typing');
                    conversationHistory.push({role: currentAgent.charAt(0).toUpperCase() + currentAgent.slice(1), content: streamContent});
                }
            } else if (data.type === 'complete') {
                isStreaming = false;
                const statusDivs = container.querySelectorAll('.status');
                statusDivs.forEach(div => div.remove());
            } else if (data.type === 'error') {
                isStreaming = false;
                addMessage('System', 'Error: ' + data.content, '#ff6b6b');
            }
            
            container.scrollTop = container.scrollHeight;
        }
        
        function setMode(mode) {
            currentMode = mode;
            document.getElementById('chatMode').classList.toggle('active', mode === 'chat');
            document.getElementById('debateMode').classList.toggle('active', mode === 'debate');
            document.getElementById('currentModeDisplay').textContent = mode === 'chat' ? 'Chat' : 'Debate';
            clearChat();
        }
        
        function clearChat() {
            document.getElementById('chatContainer').innerHTML = 
                '<div class="status">Chat cleared. Ready for new conversation.</div>';
            conversationHistory = [];
        }
        
        function updateModelDisplay() {
            // This function can be expanded later if needed
        }
        
        function updateParamDisplay(paramId, displayId) {
            const value = document.getElementById(paramId).value;
            document.getElementById(displayId).textContent = value;
        }
        
        function getModelConfig() {
            return {
                model: document.getElementById('modelSelector').value,
                temperature: parseFloat(document.getElementById('temperature').value),
                top_p: parseFloat(document.getElementById('topP').value),
                top_k: parseInt(document.getElementById('topK').value),
                max_tokens: parseInt(document.getElementById('maxTokens').value)
            };
        }
        
        function sendMessage() {
            if (isStreaming) return; // Prevent multiple simultaneous requests
            
            const input = document.getElementById('messageInput');
            const message = input.value.trim();
            if (!message) return;
            
            // Add user message
            addMessage('You', message, '#4a9eff');
            conversationHistory.push({role: 'User', content: message});
            input.value = '';
            
            // Start streaming
            startStream(currentMode === 'chat' ? 'prompt' : 'debate', message);
        }
        
        function addMessage(role, content, color = '#e0e0e0') {
            const container = document.getElementById('chatContainer');
            const div = document.createElement('div');
            div.className = 'message';
            div.innerHTML = `<strong style="color: ${color};">${role}:</strong> ${content}`;
            container.appendChild(div);
            container.scrollTop = container.scrollHeight;
        }
        
        function startStream(type, content) {
            if (!ws || ws.readyState !== WebSocket.OPEN) {
                addMessage('System', 'Connection lost. Reconnecting...', '#ff6b6b');
                initWebSocket();
                return;
            }
            
            isStreaming = true;
            
            const container = document.getElementById('chatContainer');
            const statusDiv = document.createElement('div');
            statusDiv.className = 'status';
            statusDiv.textContent = 'Streaming...';
            container.appendChild(statusDiv);
            
            ws.send(JSON.stringify({
                type: type,
                content: content,
                history: conversationHistory,
                config: getModelConfig()
            }));
        }
        
        // Initialize WebSocket when page loads
        window.onload = initWebSocket;
        
        // Global variables for streaming
        let currentAgent = '';
        let streamContent = '';
        let currentAgentDiv = null;
    </script>
</body>
</html>
"""
