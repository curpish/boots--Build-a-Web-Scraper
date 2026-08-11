import asyncio
import sys
from ast import AsyncFunctionDef

from crawl import crawl_site_async


async def main():
    args = sys.argv
    url = args[1]

    if len(sys.argv) < 4:
        print("Expected 3 arguments: base_url, max_concurrency, max_pages")
        sys.exit(1)
    if len(sys.argv) > 4:
        print("Too many arguments provided!")
        sys.exit(1)

    if not args[2].isdigit():
        print("max_concurrency must be an integer")
        sys.exit(1)
    if not args[3].isdigit():
        print("max_pages must be an integer")
        sys.exit(1)

    max_concurrency = int(args[2])
    max_pages = int(args[3])
    print(f"Hello from web-crawler-in-python! Now crawling: {url}")
    page_data = await crawl_site_async(url, max_concurrency, max_pages)

    if page_data:
        print(page_data)

    print("Script name:", sys.argv[0])  # example.py
    print("Argument:", sys.argv[1])  # -v
    base_url = sys.argv[1]
    print(f"starting crawl of: {base_url}")

    print(f"Found {len(page_data)} pages:")
    for page in page_data.values():
        print(f"- {page['url']}:\n {len(page['outgoing_links'])} outgoing links\n")


if __name__ == "__main__":
    asyncio.run(main())
