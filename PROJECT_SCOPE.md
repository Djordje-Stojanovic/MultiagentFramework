# MultiAgent Framework - Project Scope

**Living Document - Updated as we go**

## Current Focus
Building a multi-agent debate system, step by step.

## Tech Stack (Decided)
- **Framework:** Pydantic AI (simple, minimal abstraction)
- **LLMs:** 
  - Gemini 2.5 Pro (smart model for complex reasoning)
  - Gemini 2.5 Flash (fast & cheap for simple tasks)
- **Language:** Python
- **Documentation:** Trafilatura (offline, forever-free scraping)
- **MCP Servers:** GitHub only (for code management)

## Core Design Philosophy
- **Multi-Model by Design**: Never lock into a single LLM provider. Code must work with OpenAI, Anthropic, Google, OpenRouter, and any future providers.
- **Pydantic AI as Abstraction**: Our abstraction layer handles all model providers uniformly - streaming, async, sync all work the same regardless of underlying model.
- **Model Agnostic Architecture**: Agent definitions, streaming, and all functionality must work identically across GPT-4, Claude, Gemini, or any model we add.
- **Dark Mode Only**: The modern, professional standard for AI applications. No light mode elements.

## Platform Decision ✅
**Chosen: Web app with FastAPI + simple HTML**
- Start simple, iterate fast
- No complex build process
- Cross-platform by default
- Easy local development and deployment

## Folder Structure
```
MultiagentFramework/
├── Cline.md              # Main instruction file
├── PROJECT_SCOPE.md      # This file - project overview
├── README.md             # Project documentation
├── requirements.txt      # Python dependencies
├── .env                  # Environment variables (Gemini API key)
├── docs/                 # Scraped documentation
│   ├── python_intro.md
│   ├── TRAFILATURA_GUIDE.md # Complete Trafilatura usage guide
│   ├── gemini_core/      # 20 core Gemini API docs
│   ├── pydantic_core/    # 14 core Pydantic docs
│   └── trafilatura_full_docs/ # Full Trafilatura documentation
└── src/                  # Source code
    ├── hello_world.py    # Working Pydantic AI + FastAPI demo
    └── tools/            # Helper tools
        └── scrape_docs.py # Trafilatura wrapper
```

## Documentation Solution ✅
**Trafilatura** - Our chosen documentation scraper
- ✅ Installed: `py -m pip install trafilatura`
- ✅ Zero-cost: Works offline, no API keys needed
- ✅ Forever-free: No usage limits or subscriptions
- ✅ Helper script: `src/tools/scrape_docs.py`
- ✅ Guide: `docs/TRAFILATURA_GUIDE.md` with crawling/filtering strategies
- ✅ Scraped docs:
  - Gemini API: 20 core documentation files
  - Pydantic: 14 core documentation files
  - Trafilatura: Full documentation

## Next Steps
1. ✅ Decide on platform (webapp with FastAPI)
2. ✅ Create hello world with Pydantic AI
3. ✅ Setup documentation solution (Trafilatura)
4. ✅ Test hello world in action - Working with Gemini API!
5. ✅ Add auto-reload to development server
6. ✅ Create enhanced UI that shows:
   - ✅ Current model being used (gemini-2.0-flash-exp)
   - ✅ Real model settings and configuration (temperature, top-P, top-K, max_tokens)
   - ✅ Text input field for custom prompts
   - ✅ FastAPI documentation scraped (20 files)
7. ✅ Organize and rename scraped documentation
   - ✅ Rename all documentation files to meaningful camelCase names
   - ✅ Create rich JSON sitemaps with metadata for Gemini, Pydantic, and FastAPI
   - ✅ Delete old URL text files
8. ✅ Get two agents talking to each other
   - ✅ Implemented Agent 1 (discussion initiator) and Agent 2 (counter-argument provider)
   - ✅ Created /debate endpoint for three-step conversation flow
   - ✅ Added Two-Agent Conversation section to GUI
   - ✅ Real-time debate visualization with clear agent roles
   - ✅ Tested with complex topics (WW2 Germany performance debate)
9. ⬜ **NEXT:** Improve UI design and user experience
9.1. ✅ **COMPLETED:** Implement dark mode only philosophy
   - ✅ Converted entire UI to beautiful, modern dark mode
   - ✅ Removed all light mode elements
   - ✅ Following dark mode as the professional standard for AI applications
   - ✅ Added dark mode philosophy to Cline.md development guidelines
9.2. ✅ **COMPLETED:** Implement Live Token Streaming
   - ✅ Fixed Pydantic AI streaming with proper `async with agent.run_stream()` syntax
   - ✅ Real-time token streaming for both Chat and Debate modes
   - ✅ Conversation memory - agents remember previous messages in context
   - ✅ Generic agent architecture - no hardcoded "Agent 1/2" references
   - ✅ Applied Elon's algorithm: Split bloated files following 200 LOC limit
     - `hello_world.py`: 41 lines (main FastAPI app)
     - `streaming.py`: 149 lines (WebSocket streaming logic)
     - `ui.py`: 178 lines (HTML/JS interface)
     - `styles.py`: 46 lines (CSS styling)
   - ✅ Small surgical changes only - no feature bloat, modular architecture
   - ✅ **CRITICAL BUGS FIXED:**
     - Fixed f-string syntax error with JavaScript template literals
     - Restored model configuration panel (was removed during refactoring)
     - Fixed WebSocket duplicate ID bug with unique timestamps
     - Proper DOM cleanup to prevent streaming element conflicts
     - Used Python VSCode extension for better error detection
   - ✅ **USER TESTED:** Live streaming working perfectly with conversation memory

9.3. ✅ **COMPLETED:** Critical Production Issues Resolved
   - ✅ **Fixed Pydantic AI Configuration Error**: Resolved `Unknown keyword arguments: model_kwargs` by implementing proper `ModelSettings` approach
     - Replaced invalid `model_kwargs` parameter with correct `ModelSettings(temperature, top_p, max_tokens)`
     - Applied settings per-request using `agent.run_stream(prompt, model_settings=model_settings)`
     - Note: `top_k` parameter not available in Pydantic AI (only top_p supported)
   - ✅ **Fixed WebSocket Memory Loss**: Resolved frequent disconnections causing conversation history reset
     - Removed `ws.close()` that was causing disconnections on every message
     - Implemented persistent WebSocket connection with auto-reconnect logic
     - Added `isStreaming` flag to prevent multiple simultaneous requests
     - **Verified**: Conversation memory now works perfectly (agents remember context across messages)
   - ✅ **WebSocket Behavior Research**: Confirmed logging patterns are normal and healthy
     - Used Google AI research to verify open/close cycles are standard FastAPI/Uvicorn lifecycle events
     - Confirmed application follows 2024-2025 WebSocket best practices for chat applications
     - No actual performance issues or connectivity problems detected
   - ✅ **Enhanced Debugging**: Added WebSocket close code logging to distinguish normal vs problematic disconnections
     - Logs close codes with normal (1000/1001) vs abnormal (1006/1002/1011) classification
     - Improved error handling with connection state checks
     - Better diagnostic information for future troubleshooting

## Phase 10: Future Enhancement Opportunities

10.1. **SUGGESTED:** Enhanced Agent Personalities & Custom Instructions
   - Add configurable agent personalities (analytical, creative, contrarian, etc.)
   - Custom system prompts per agent for specialized roles
   - Agent memory persistence across sessions
   - Pre-built agent templates (researcher, critic, optimist, etc.)

10.2. **SUGGESTED:** Multi-Model Support & Model Comparison
   - Support multiple LLM providers (OpenAI, Anthropic, local models)
   - Side-by-side model comparison in debates
   - Model switching during conversations
   - Performance metrics and response quality comparison

10.3. **SUGGESTED:** Advanced Conversation Features
   - Export conversations to markdown/PDF
   - Conversation branching (save/load conversation states)
   - Topic summarization after long discussions
   - Search through conversation history
   - Conversation templates for specific use cases
10. ⬜ Add debate logic and winner selection

## What We're Building (MVP)
- Two agents that debate a topic
- Simple UI to watch the debate
- Basic winner selection

## Current Status
✅ **Two-Agent Conversation System Complete!**
- Pydantic AI connected to Gemini API
- FastAPI server with auto-reload
- Enhanced web interface at http://localhost:8000
- Real Gemini API configuration parameters displayed
- Custom prompt interface working
- Complete documentation sets: Gemini (20), Pydantic (14), FastAPI (20)
- All progress committed to GitHub
- ✅ **Documentation Organized!**
  - All scraped documentation has been renamed to meaningful camelCase names.
  - Rich JSON sitemaps with metadata have been created for Gemini, Pydantic, and FastAPI.
  - Old URL text files have been removed.
- ✅ **Two-Agent Debate System Working!**
  - Agent 1 initiates discussions, Agent 2 provides counter-arguments
  - Three-step conversation flow: Agent1 → Agent2 → Agent1 final reply
  - Visual agent roles clearly displayed in model configuration
  - Real-time debate visualization in GUI
  - Tested with sophisticated topics and complex reasoning

---
*Updated: August 10, 2025 - 11:32 AM - Added Pydantic AI fixes and WebSocket debugging enhancements*
