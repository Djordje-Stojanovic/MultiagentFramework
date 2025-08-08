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
6. ⬜ **NEXT:** Create enhanced UI that shows:
   - Current model being used (gemini-2.0-flash-exp)
   - Model settings and configuration
   - Text input field for custom prompts
7. ⬜ Get two agents talking to each other
8. ⬜ Add debate logic

## What We're Building (MVP)
- Two agents that debate a topic
- Simple UI to watch the debate
- Basic winner selection

## Current Status
✅ **Hello World Working!**
- Pydantic AI connected to Gemini API
- FastAPI server with auto-reload
- Simple web interface at http://localhost:8000
- Agent responds to prompts successfully

---
*Updated: January 8, 2025 - 11:47 PM*
