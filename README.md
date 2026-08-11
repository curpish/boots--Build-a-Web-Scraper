# Async Web Crawler

A concurrent, async web crawler built in Python. It crawls a target site,
follows internal links, and reports on the pages it finds — including
headings, first paragraphs, outgoing links, and images.

## Features

- **Async crawling** with aiohttp for non-blocking HTTP requests
- **Concurrency control** via a semaphore, so you can tune how many
  requests run at once
- **Page limiting** so the crawler stops gracefully once it's visited
  a configurable number of pages
- **Same-domain filtering** — only follows links within the site
  you're crawling
- **HTML parsing** with BeautifulSoup to extract headings, first
  paragraphs, links, and images

## Usage

  uv run main.py <base_url> <max_concurrency> <max_pages>

Example:

  uv run main.py https://example.com 3 10

This crawls https://example.com, running up to 3 requests concurrently,
and stops after 10 pages have been visited.

## How It Works

1. The crawler starts at base_url and fetches its HTML.
2. It extracts outgoing links, images, headings, and the first paragraph.
3. Each internal link found is scheduled as its own async task, so many
   pages can be fetched in parallel (bounded by max_concurrency).
4. A shared page_data dictionary (protected by a lock) tracks visited
   pages to avoid duplicate work.
5. Once max_pages is reached, the crawler flips a should_stop flag
   and cancels any in-flight tasks, so the program exits cleanly instead
   of continuing to spawn new requests.

## Running Tests

  uv run pytest

## Requirements

- Python 3.10+
- uv for dependency management (https://docs.astral.sh/uv/)
- aiohttp, beautifulsoup4
