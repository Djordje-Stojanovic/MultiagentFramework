"""
CSS Styles for MultiAgent Framework
Separated per Elon's algorithm to keep files under 200 LOC
"""

def get_css():
    """Returns the CSS styles"""
    return """
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', roboto, sans-serif;
            background: #0a0a0a; color: #e0e0e0; line-height: 1.6;
            min-height: 100vh; display: flex; flex-direction: column;
        }
        .container { max-width: 800px; margin: 0 auto; padding: 20px; flex: 1; }
        h1 { text-align: center; margin-bottom: 30px; color: #fff; font-weight: 300; }
        .mode-selector { display: flex; gap: 10px; margin-bottom: 20px; justify-content: center; }
        button {
            background: #1a1a1a; color: #e0e0e0; border: 1px solid #333; 
            padding: 12px 24px; border-radius: 8px; cursor: pointer; 
            transition: all 0.3s ease; font-size: 14px;
        }
        button:hover { background: #2a2a2a; }
        button.active { background: #2d7a2d; border-color: #2d7a2d; color: white; }
        .chat-container {
            background: #1a1a1a; border-radius: 12px; padding: 20px;
            margin-bottom: 20px; min-height: 400px; border: 1px solid #333;
        }
        .input-container { display: flex; gap: 10px; }
        input[type="text"] {
            flex: 1; background: #222; color: #e0e0e0; border: 1px solid #444;
            padding: 12px; border-radius: 8px; font-size: 14px;
        }
        input[type="text"]:focus { outline: none; border-color: #2d7a2d; }
        .send-btn { background: #2d7a2d; color: white; }
        .send-btn:hover { background: #359935; }
        .message { margin-bottom: 15px; }
        .status { color: #888; font-style: italic; margin-bottom: 10px; }
        .agent-response { background: #262626; padding: 15px; border-radius: 8px; margin: 10px 0; }
        .typing { opacity: 0.7; }
        .config-panel {
            background: #1a1a1a; border-radius: 12px; padding: 20px;
            margin-bottom: 20px; border: 1px solid #333;
        }
        .config-grid {
            display: grid; grid-template-columns: 1fr 1fr;
            gap: 15px; margin-top: 15px;
        }
        .config-item {
            background: #222; padding: 10px; border-radius: 6px;
            border-left: 4px solid #2d7a2d;
        }
    """
