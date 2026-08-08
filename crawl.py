from urllib.parse import urlsplit

from bs4 import BeautifulSoup, Tag


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
