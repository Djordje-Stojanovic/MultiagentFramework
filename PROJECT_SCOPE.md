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
*Updated: January 9, 2025 - 1:07 AM*
