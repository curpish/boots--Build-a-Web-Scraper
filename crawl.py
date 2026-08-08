from typing import TypedDict
from urllib.parse import urljoin, urlsplit

from bs4 import BeautifulSoup, Tag

class PageData(TypedDict):
    url: str
    heading: str
    first_paragraph: str
    outgoing_links: list[str]
    image_urls: list[str]

def normalize_url(input_url):
    o = urlsplit(input_url)
    clean_rear = o.path.rstrip("/")
    normalized = o.netloc + clean_rear
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
