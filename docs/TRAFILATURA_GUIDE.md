# Trafilatura Documentation Scraper Guide

## Why Trafilatura?

Trafilatura is the ideal documentation scraping solution because it's:
- **100% Offline** - No API keys, no rate limits, no SaaS dependencies
- **Battle-tested** - Used in production by Hugging Face and major data pipelines
- **Simple** - Direct CLI commands or Python script usage
- **Efficient** - Fast, lightweight, and preserves only the main content
- **Forever Free** - Open-source, runs locally, no pricing changes ever

## Installation

Already installed! But for reference:
```bash
py -m pip install trafilatura
```

## Quick Usage Guide

### 1. Using Trafilatura CLI Directly

#### Single Page to Markdown
```bash
trafilatura -u "https://docs.python.org/3/tutorial/" --markdown > python_tutorial.md
```

#### Crawl/Spider Entire Website (NEW!)
```bash
# Crawl from a starting URL and follow links automatically
trafilatura --crawl "https://ai.google.dev/gemini-api/docs" --max-downloads 50 -o docs/output/ --markdown

# This will:
# - Start from the given URL
# - Automatically discover and follow links on the same domain
# - Download up to 50 pages (adjust as needed)
# - Save everything to the output folder as markdown files
```

#### Batch Processing from URL List
Create a `urls.txt` file with one URL per line, then:
```bash
trafilatura -i urls.txt -o docs_scraped/ --markdown
```

#### Find & Use Sitemaps (IMPORTANT!)
```bash
# Most sites have sitemaps at these locations:
# - /sitemap.xml
# - /sitemap_index.xml
# - /robots.txt (often lists sitemap location)

# Example: Find Gemini's sitemap
# Try: https://ai.google.dev/sitemap.xml
# Or check: https://ai.google.dev/robots.txt

# List ALL URLs from sitemap (WARNING: Can be thousands!)
trafilatura --sitemap "https://docs.python.org/3/sitemap.xml" --list > all_urls.txt

# Count how many URLs before scraping
type all_urls.txt | find /c /v ""
```

#### Filter & Scrape Only What You Need
```bash
# STEP 1: Get all URLs from sitemap
trafilatura --sitemap "https://ai.google.dev/sitemap.xml" --list > all_urls.txt

# STEP 2: Filter to only what you need (Windows)
# For Gemini API docs only:
type all_urls.txt | findstr /gemini-api/docs > gemini_filtered.txt

# For specific sections:
type all_urls.txt | findstr /tutorial/ > tutorial_urls.txt
type all_urls.txt | findstr /quickstart > quickstart_urls.txt

# STEP 3: Scrape ONLY the filtered URLs
trafilatura -i gemini_filtered.txt -o docs/gemini/ --markdown

# Pro tip: Combine multiple filters
type all_urls.txt | findstr "function-calling structured-output long-context" > key_features.txt
```

#### Smart Selective Scraping
```bash
# Instead of downloading 1000s of pages, be strategic:

# 1. Core documentation only (usually <50 pages)
echo https://ai.google.dev/gemini-api/docs > core_urls.txt
echo https://ai.google.dev/gemini-api/docs/quickstart >> core_urls.txt
echo https://ai.google.dev/gemini-api/docs/text-generation >> core_urls.txt
echo https://ai.google.dev/gemini-api/docs/function-calling >> core_urls.txt
echo https://ai.google.dev/gemini-api/docs/structured-output >> core_urls.txt
trafilatura -i core_urls.txt -o docs/gemini_core/ --markdown

# 2. Use --max-downloads with crawl for controlled scraping
trafilatura --crawl "https://ai.google.dev/gemini-api/docs" --max-downloads 30 -o docs/gemini_essential/ --markdown
```

### 2. Using the Python Script (scrape_docs.py)

#### Single Page
```bash
# Display to console
py scrape_docs.py https://docs.python.org/3/tutorial/

# Save to file
py scrape_docs.py https://docs.python.org/3/tutorial/ --output python_tutorial.md
```

#### From Sitemap
```bash
# Scrape entire sitemap
py scrape_docs.py --sitemap https://docs.python.org/3/sitemap.xml

# Filter to specific path
py scrape_docs.py --sitemap https://docs.python.org/3/sitemap.xml --filter /tutorial/
```

## Real-World Examples

### 0. Crawl Entire Documentation Sites (NEW!)
```bash
# Crawl Gemini API docs (follow links from main page)
trafilatura --crawl "https://ai.google.dev/gemini-api/docs" --max-downloads 100 -o docs/gemini_full/ --markdown

# Crawl Pydantic docs
trafilatura --crawl "https://docs.pydantic.dev/latest/" --max-downloads 100 -o docs/pydantic_full/ --markdown

# Note: --crawl automatically discovers and follows links on the same domain
# Adjust --max-downloads based on site size (or omit for unlimited)
```

### 1. Scrape Next.js Documentation
```bash
# Get the App Router docs
trafilatura -u "https://nextjs.org/docs/app" --markdown > docs_scraped/nextjs_app_router.md
```

### 2. Scrape FastAPI Documentation
```bash
# Single important page
trafilatura -u "https://fastapi.tiangolo.com/tutorial/" --markdown > docs_scraped/fastapi_tutorial.md
```

### 3. Scrape React Documentation
```bash
# Get React Hooks documentation
trafilatura -u "https://react.dev/reference/react" --markdown > docs_scraped/react_hooks.md
```

### 4. Scrape Tailwind CSS
```bash
# Get utility classes reference
trafilatura -u "https://tailwindcss.com/docs/utility-first" --markdown > docs_scraped/tailwind_utilities.md
```

## Directory Structure

```
MultiagentFramework/
├── docs_scraped/           # All scraped documentation goes here
│   ├── python_intro.md     # Example: Python introduction
│   ├── nextjs_routing.md   # Example: Next.js routing docs
│   └── ...                 # Other scraped docs
├── scrape_docs.py          # Python helper script
└── TRAFILATURA_GUIDE.md    # This guide
```

## Pro Tips

### 1. Keep Documentation Organized
Create subdirectories for different projects:
```bash
mkdir docs_scraped/python
mkdir docs_scraped/javascript
mkdir docs_scraped/frameworks
```

### 2. Create a Scraping List
Maintain a file with commonly needed documentation:
```text
# docs_to_scrape.txt
https://docs.python.org/3/tutorial/
https://nextjs.org/docs/app/building-your-application/routing
https://fastapi.tiangolo.com/tutorial/first-steps/
https://react.dev/learn
```

Then batch scrape:
```bash
trafilatura -i docs_to_scrape.txt -o docs_scraped/ --markdown
```

### 3. Update Documentation Periodically
Create a simple update script:
```bash
# update_docs.bat
@echo off
echo Updating documentation...
trafilatura -i docs_to_scrape.txt -o docs_scraped/ --markdown --no-comments
echo Documentation updated!
```

### 4. Use with AI Coding
When using Cline or other AI coding assistants:
1. Scrape relevant docs before starting a project
2. Reference them in your prompts: "Using the FastAPI documentation in docs_scraped/fastapi_tutorial.md..."
3. The AI will have accurate, up-to-date information

## Advantages Over Alternatives

| Tool | Pros | Cons |
|------|------|------|
| **Trafilatura** | ✅ Free forever, ✅ Offline, ✅ Fast, ✅ Reliable | - |
| Context7 | Good UX | ❌ API based, ❌ Token limits |
| Ref.tools | Token efficient | ❌ Requires API key, ❌ Paid tiers |
| SlurpAI | Lightweight | ❌ Less mature, ❌ Limited features |
| Firecrawl | Great UX | ❌ Credit system, ❌ Not free |
| Jina Reader | Zero install | ❌ Hosted service, ❌ Not a crawler |

## Common Use Cases

### Before Starting a New Project
```bash
# Scrape framework docs
trafilatura -u "https://nextjs.org/docs" --markdown > docs_scraped/nextjs_main.md

# Scrape library docs
trafilatura -u "https://tanstack.com/query/latest/docs" --markdown > docs_scraped/tanstack_query.md
```

### When Debugging
```bash
# Get specific error/troubleshooting pages
trafilatura -u "https://nextjs.org/docs/messages/react-hydration-error" --markdown > docs_scraped/hydration_error.md
```

### Learning New Technologies
```bash
# Create a learning folder
mkdir docs_scraped/learning_rust
trafilatura --sitemap "https://doc.rust-lang.org/sitemap.xml" --list | findstr /book/ > rust_book_urls.txt
trafilatura -i rust_book_urls.txt -o docs_scraped/learning_rust/ --markdown
```

## Troubleshooting

### Issue: Some pages don't extract well
**Solution**: Use `--fallback` option for JavaScript-heavy sites:
```bash
trafilatura -u "https://example.com" --markdown --fallback
```

### Issue: Too much content scraped
**Solution**: Use `--max-downloads` to limit:
```bash
trafilatura --sitemap "https://example.com/sitemap.xml" --max-downloads 10 --markdown
```

### Issue: Want to exclude certain content
**Solution**: Use `--no-comments` and `--no-tables` flags:
```bash
trafilatura -u "https://example.com" --markdown --no-comments --no-tables
```

## Advanced Features

### Web Crawling/Spidering
Trafilatura can automatically crawl websites and follow links:
- **--crawl**: Start from a URL and automatically follow links
- **--max-downloads**: Limit the number of pages to scrape
- Intelligent link discovery on the same domain
- Full documentation available in `docs/trafilatura_full_docs/`

## Summary

Trafilatura is your reliable, offline, forever-free documentation scraping solution. It's perfect for:
- Building local documentation libraries
- Providing context to AI coding assistants
- Creating offline documentation backups
- Learning new technologies without internet dependency

No API keys, no rate limits, no subscription tiers - just pure, efficient documentation extraction that will keep working forever.
