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

## Next Decision Required
**Platform choice:**
1. **Web app** (FastAPI + React/simple HTML)
   - Pros: Easy deployment, cross-platform, no installation
   - Cons: Need server, more moving parts

2. **Electron app** (Web tech in desktop wrapper)
   - Pros: Desktop app feel, web tech stack, cross-platform
   - Cons: Bloated, resource heavy

3. **Native Windows** (PyQt or Tkinter)
   - Pros: Lightweight, native performance
   - Cons: Windows only, UI might look dated

## Next Steps
1. ⬜ Decide on platform (webapp/electron/native)
2. ⬜ Create hello world with Pydantic AI
3. ⬜ Get two agents talking to each other
4. ⬜ Add debate logic

## What We're Building (MVP)
- Two agents that debate a topic
- Simple UI to watch the debate
- Basic winner selection

That's it. We'll figure out the rest as we go.

---
*Updated: August 8, 2025*
