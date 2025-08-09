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
                    <strong>Model:</strong> gemini-2.0-flash-exp
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
        
        function sendMessage() {
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
            if (ws) ws.close();
            
            const container = document.getElementById('chatContainer');
            
            // Clean up any existing streaming elements
            const existingStreaming = container.querySelectorAll('[id^="streaming-"]');
            existingStreaming.forEach(el => {
                if (el.classList.contains('typing')) {
                    el.classList.remove('typing');
                }
            });
            
            const statusDiv = document.createElement('div');
            statusDiv.className = 'status';
            statusDiv.textContent = 'Connecting...';
            container.appendChild(statusDiv);
            
            ws = new WebSocket(`ws://localhost:8000/ws`);
            let currentAgent = '';
            let streamContent = '';
            let currentAgentDiv = null;
            
            ws.onopen = () => {
                statusDiv.textContent = 'Streaming...';
                ws.send(JSON.stringify({
                    type: type,
                    content: content,
                    history: conversationHistory
                }));
            };
            
            ws.onmessage = (event) => {
                const data = JSON.parse(event.data);
                
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
                    if (statusDiv.parentNode) {
                        statusDiv.remove();
                    }
                } else if (data.type === 'error') {
                    statusDiv.textContent = 'Error: ' + data.content;
                    statusDiv.style.color = '#ff6b6b';
                }
                
                container.scrollTop = container.scrollHeight;
            };
            
            ws.onerror = () => {
                statusDiv.textContent = 'Connection error';
                statusDiv.style.color = '#ff6b6b';
            };
        }
    </script>
</body>
</html>
"""
