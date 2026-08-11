import asyncio
from typing import TypedDict
from urllib.parse import urljoin, urlparse, urlsplit

import aiohttp
import requests
from bs4 import BeautifulSoup, Tag

from exceptions import InvalidContentTypeError, RequestFailedError


class PageData(TypedDict):
    url: str
    heading: str
    first_paragraph: str
    outgoing_links: list[str]
    image_urls: list[str]

class AsyncCrawler:
    def __init__(self, base_url: str, max_concurrency: int = 10):
        self.base_url = base_url
        self.base_domain = urlparse(base_url).netloc
        self.page_data: dict[str, PageData] = {}
        self.lock = asyncio.Lock()
        self.max_concurrency = max_concurrency
        self.semaphore = asyncio.Semaphore(max_concurrency)
        self.session = None

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self


    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.session.close()

    async def add_page_visit(self, normalized_url):
        async with self.lock:
            if normalized_url not in self.page_data:
                self.page_data[normalized_url] = {
                    "url": normalized_url,
                    "heading": "",
                    "first_paragraph": "",
                    "outgoing_links": [],
                    "image_urls": [],
                }
                return True
            return False

    async def get_html(self, url: str) -> str:
        try:
            if self.session is None:
                raise RequestFailedError(f"Session not initialized for {url}")
            async with self.session.get(url, headers={"User-Agent": "BootCrawler/1.0"}) as response:
                if response.status >= 400:
                    raise RequestFailedError(
                        f"HTTP {response.status} fetching {url}: {response.reason}"
                    )

                content_type = response.headers.get("content-type", "").lower()
                if "text/html" not in content_type:
                    raise InvalidContentTypeError(
                        f"Expected 'text/html', got '{content_type}' at {url}"
                    )

                return await response.text()
        except aiohttp.ClientError as e:
            raise RequestFailedError(f"Network error fetching {url}: {e}") from e

    async def crawl_page(self,current_url: str) -> None:
        if urlsplit(current_url).netloc != self.base_domain:
            return
        normalized_url = normalize_url(current_url)
        if not await self.add_page_visit(normalized_url):
            print(f"Already crawled: {normalized_url}")
            return
        async with self.semaphore:
            try:
                html = await self.get_html(current_url)
            except Exception as e:
                async with self.lock:
                    print(f"Failed to crawl {normalized_url}: {e}")
                    self.page_data[normalized_url] = {
                        "url": current_url,
                        "heading": "",
                        "first_paragraph": "",
                        "outgoing_links": [],
                        "image_urls": [],
                    }
                return
        # semaphore released
        page_info = extract_page_data(html, current_url)
        async with self.lock:
            self.page_data[normalized_url] = page_info
            print(f"Crawled and extracted: {normalized_url}")

        tasks = []
        for link in get_urls_from_html(html, current_url):
            task = asyncio.create_task(self.crawl_page(link))
            tasks.append(task)

        if tasks:
            await asyncio.gather(*tasks)

    async def crawl(self) -> dict[str, PageData]:
        await self.crawl_page(self.base_url)
        return self.page_data

async def crawl_site_async(url: str) -> dict[str, PageData]: #not a class method
    async with AsyncCrawler(url) as crawler:
        return await crawler.crawl()

def normalize_url(input_url):
    o = urlsplit(input_url)
    clean_end = o.path.rstrip("/")
    normalized = o.netloc + clean_end
    return normalized

def get_heading_from_html(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    h_tag = soup.find("h1" if soup.find("h1") else "h2")
    return h_tag.get_text(strip=True) if isinstance(h_tag, Tag) else ""

def get_first_paragraph_from_html(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    #searching for the <main> tag if it exists and find the first <p> tag
    # within it, if it doesn't exist fallback to just
    # the first <p> tag.
    p_tag = soup.find("main")
    if p_tag is None:
        p_tag = soup.find("p")
    return p_tag.get_text(strip=True) if isinstance(p_tag, Tag) else ""

def get_urls_from_html(html, base_url):
    # base_url is the root URL of the website we're crawling.
    # This will allow us to rewrite relative URLs into absolute URLs.
    # returns an un-normalized list of all the absolute URLs found within the HTML,
    # and an error if one occurs.
    soup = BeautifulSoup(html, "html.parser")
    results = []
    tags = soup.find_all("a", href=True)
    for tag in tags:
        # safely get the value; returns None if 'href' key is missing
        href = tag.get("href")

        # ensure href exists and is a non-empty string
        if href:
            try:
                full_url = urljoin(base_url, href)
                results.append(full_url)
            except ValueError:
                # ignore invalid URLs and provide error
                print(f"Invalid URL: {href}")
    return results

def get_images_from_html(html, base_url):
    # html is an HTML string
    # base_url is the root URL of the website we're crawling.
    # This will allow us to rewrite relative URLs into absolute URLs.
    # It returns an un-normalized list of all the image URLs found within the HTML,
    # and an error if one occurs.
    soup = BeautifulSoup(html, "html.parser")
    results = []
    tags = soup.find_all("img", src=True)
    for tag in tags:
        # safely get the value; returns None if 'src' key is missing
        src = tag.get("src")
        if src:
            try:
                full_url = urljoin(base_url, src)
                results.append(full_url)
            except ValueError:
                # ignore invalid URLs and provide error
                print(f"Invalid image URL: {src}")
    return results

def extract_page_data(html: str, page_url: str) -> PageData:
    # html is an HTML string
    # page_url is the absolute URL of the page (used for converting relative URLs)
    # It returns a dictionary with keys: url, heading, first_paragraph, outgoing_links, image_urls
    return {
        "url": page_url,
        "heading": get_heading_from_html(html),
        "first_paragraph": get_first_paragraph_from_html(html),
        "outgoing_links": get_urls_from_html(html, page_url),
        "image_urls": get_images_from_html(html, page_url),
    }

def get_html(url: str) -> str:
    try:
        response = requests.get(url, headers={"User-Agent": "BootCrawler/1.0"})
    except requests.RequestException as e:
        raise RequestFailedError(f"Network error fetching {url}: {e}") from e

    if response.status_code >= 400:
        raise RequestFailedError(
            f"HTTP {response.status_code} fetching {url}: {response.reason}"
        )

    content_type = response.headers.get("content-type", "").lower()
    if "text/html" not in content_type:
        raise InvalidContentTypeError(
            f"Expected 'text/html', got '{content_type}' at {url}"
        )

    return response.text

def crawl_page(
    base_url: str,
    current_url: str | None = None,
    page_data: dict[str, PageData] | None = None,
) -> dict[str, PageData]:
    #Make sure the current_url is on the same domain as the base_url. If it's not, just return.
    if current_url is None:
        current_url = base_url
    if page_data is None:
        page_data = {}
    if urlsplit(current_url).netloc != urlsplit(base_url).netloc:
        return page_data
    normalized_url = normalize_url(current_url)
    if normalized_url in page_data:
        print(f"Already crawled: {normalized_url}")
        return page_data
    try:
        html = get_html(current_url)
        page_info = extract_page_data(html, current_url)
        page_data[normalized_url] = page_info
        print(f"Crawled and extracted: {normalized_url}")
        for link in get_urls_from_html(html, base_url):
            page_data = crawl_page(base_url, link, page_data)
    except Exception as e:
        print(f"Failed to crawl {normalized_url}: {e}")
        page_data[normalized_url] = {
            "url": current_url,
            "heading": "",
            "first_paragraph": "",
            "outgoing_links": [],
            "image_urls": [],
        }
    return page_data
