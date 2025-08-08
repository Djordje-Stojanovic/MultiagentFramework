#!/usr/bin/env python3
"""
Simple documentation scraper using Trafilatura
Usage: 
  python scrape_docs.py <url> [--output <filename>]
  python scrape_docs.py --sitemap <sitemap_url> [--filter <path>]
"""

import argparse
import os
import sys
from pathlib import Path
import trafilatura
from trafilatura.sitemaps import sitemap_search
from trafilatura.settings import use_config

def scrape_single_page(url, output_file=None):
    """Scrape a single page and save as markdown"""
    print(f"Scraping: {url}")
    
    # Download the page
    downloaded = trafilatura.fetch_url(url)
    if not downloaded:
        print(f"Failed to download: {url}")
        return False
    
    # Extract content as markdown
    result = trafilatura.extract(downloaded, output_format='markdown', include_links=True)
    
    if result:
        if output_file:
            output_path = Path("docs_scraped") / output_file
            output_path.parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(result)
            print(f"Saved to: {output_path}")
        else:
            print(result)
        return True
    else:
        print(f"No content extracted from: {url}")
        return False

def scrape_from_sitemap(sitemap_url, filter_path=None):
    """Scrape all pages from a sitemap"""
    print(f"Fetching sitemap: {sitemap_url}")
    
    # Get URLs from sitemap
    urls = sitemap_search(sitemap_url)
    
    if not urls:
        print("No URLs found in sitemap")
        return
    
    # Filter URLs if path specified
    if filter_path:
        urls = [url for url in urls if filter_path in url]
        print(f"Filtered to {len(urls)} URLs containing '{filter_path}'")
    else:
        print(f"Found {len(urls)} URLs in sitemap")
    
    # Create output directory
    output_dir = Path("docs_scraped")
    output_dir.mkdir(exist_ok=True)
    
    # Process each URL
    for i, url in enumerate(urls, 1):
        print(f"\n[{i}/{len(urls)}] Processing: {url}")
        
        # Create filename from URL
        filename = url.replace('https://', '').replace('http://', '')
        filename = filename.replace('/', '_').replace('?', '_').replace('&', '_')
        filename = f"{filename[:100]}.md"  # Limit filename length
        
        scrape_single_page(url, filename)
    
    print(f"\nCompleted! Scraped {len(urls)} pages to docs_scraped/")

def main():
    parser = argparse.ArgumentParser(description='Scrape documentation using Trafilatura')
    parser.add_argument('url', nargs='?', help='URL to scrape')
    parser.add_argument('--output', '-o', help='Output filename (for single page)')
    parser.add_argument('--sitemap', '-s', help='Scrape from sitemap URL')
    parser.add_argument('--filter', '-f', help='Filter sitemap URLs by path')
    
    args = parser.parse_args()
    
    if args.sitemap:
        scrape_from_sitemap(args.sitemap, args.filter)
    elif args.url:
        scrape_single_page(args.url, args.output)
    else:
        print("Usage:")
        print("  Single page:  python scrape_docs.py <url> [--output <filename>]")
        print("  From sitemap: python scrape_docs.py --sitemap <sitemap_url> [--filter <path>]")
        print("\nExamples:")
        print("  python scrape_docs.py https://docs.python.org/3/tutorial/")
        print("  python scrape_docs.py --sitemap https://docs.python.org/3/sitemap.xml --filter /tutorial/")

if __name__ == '__main__':
    main()
