import unittest

from crawl import (
    extract_page_data,
    get_first_paragraph_from_html,
    get_heading_from_html,
    get_images_from_html,
    get_urls_from_html,
    normalize_url,
)


class TestCrawl(unittest.TestCase):
## start url normalize tests ##
    def test_normalize_url(self):
        input_url = "https://www.boot.dev/blog/path"
        actual = normalize_url(input_url)
        expected = "www.boot.dev/blog/path"
        self.assertEqual(actual, expected)
    def test_case_sensitive(self):
        input_url = "https://www.Boot.dev/blog/path"
        actual = normalize_url(input_url)
        expected = "www.Boot.dev/blog/path"
        self.assertEqual(actual, expected)
    def test_blank(self):
        input_url = ""
        actual = normalize_url(input_url)
        expected = ""
        self.assertEqual(actual, expected)
    def test_http_only(self):
        input_url = "http://www.boot.dev/blog/path"
        actual = normalize_url(input_url)
        expected = "www.boot.dev/blog/path"
        self.assertEqual(actual, expected)
    def test_https_trailing_slash(self):
        input_url = "https://www.boot.dev/blog/path/"
        actual = normalize_url(input_url)
        expected = "www.boot.dev/blog/path"
        self.assertEqual(actual, expected)
    def test_http_trailing_slash(self):
        input_url = "http://www.boot.dev/blog/path/"
        actual = normalize_url(input_url)
        expected = "www.boot.dev/blog/path"
        self.assertEqual(actual, expected)
## start get heading tests ##
    def test_get_heading_from_html(self):
        html = "<h1></h1>"
        actual = get_heading_from_html(html)
        expected = ""
        self.assertEqual(actual, expected)
    def test_get_heading_from_html_with_content(self):
        html = "<h1>Hello</h1>"
        actual = get_heading_from_html(html)
        expected = "Hello"
        self.assertEqual(actual, expected)
    def test_get_heading_h2(self):
        html = "<h2></h2>"
        actual = get_heading_from_html(html)
        expected = ""
        self.assertEqual(actual, expected)
    def test_get_heading_no_heading(self):
        html = "<div></div>"
        actual = get_heading_from_html(html)
        expected = ""
        self.assertEqual(actual, expected)
    def test_get_heading_no_tags(self):
        html = ""
        actual = get_heading_from_html(html)
        expected = ""
        self.assertEqual(actual, expected)
## get_first_paragraph tests ##
    def test_get_first_paragraph_empty_with_tags(self):
        html = "<p></p>"
        actual = get_first_paragraph_from_html(html)
        expected = ""
        self.assertEqual(actual, expected)
    def test_get_first_paragraph_no_tag(self):
        html = ""
        actual = get_first_paragraph_from_html(html)
        expected = ""
        self.assertEqual(actual, expected)
    def test_get_first_paragraph_with_content(self):
        html = "<p>Hello, world!</p>"
        actual = get_first_paragraph_from_html(html)
        expected = "Hello, world!"
        self.assertEqual(actual, expected)
## get_urls_from_html tests ##
    def test_get_urls_from_html_absolute(self):
        input_url = "https://crawler-test.com"
        input_body = '<html><body><a href="https://crawler-test.com"><span>Boot.dev</span></a></body></html>'
        actual = get_urls_from_html(input_body, input_url)
        expected = ["https://crawler-test.com"]
        self.assertEqual(actual, expected)
    def test_get_urls_from_html_multiple_urls(self):
        input_url = "https://crawler-test.com"
        input_body = '<html><body><a href="https://crawler-test.com"><span>Boot.dev</span></a><a href="https://crawler-test.com/about"><span>About</span></a></body></html>'
        actual = get_urls_from_html(input_body, input_url)
        expected = ["https://crawler-test.com", "https://crawler-test.com/about"]
        self.assertEqual(actual, expected)
    def test_get_urls_from_html_relative(self):
        input_url = "https://crawler-test.com"
        input_body = '<html><body><a href="/about"><span>About</span></a></body></html>'
        actual = get_urls_from_html(input_body, input_url)
        expected = ["https://crawler-test.com/about"]
        self.assertEqual(actual, expected)
## get_images_from_html tests ##
    def test_get_images_from_html_relative(self):
        input_url = "https://crawler-test.com"
        input_body = '<html><body><img src="/logo.png" alt="Logo"></body></html>'
        actual = get_images_from_html(input_body, input_url)
        expected = ["https://crawler-test.com/logo.png"]
        self.assertEqual(actual, expected)
    def test_get_images_from_html_attribute_missing(self):
        input_url = "https://crawler-test.com"
        input_body = '<html><body><img alt="Logo"></body></html>'
        actual = get_images_from_html(input_body, input_url)
        expected = []
        self.assertEqual(actual, expected)
    def test_get_images_from_html_clean_absolute(self):
        input_url = "https://crawler-test.com"
        input_body = '<html><body><img src="https://crawler-test.com/logo.png" alt="Logo"></body></html>'
        actual = get_images_from_html(input_body, input_url)
        expected = ["https://crawler-test.com/logo.png"]
        self.assertEqual(actual, expected)
## extract_page_data tests ##
    def test_extract_page_data_basic(self):
        input_url = "https://crawler-test.com"
        input_body = """<html><body>
            <h1>Test Title</h1>
            <p>This is the first paragraph.</p>
            <a href="/link1">Link 1</a>
            <img src="/image1.jpg" alt="Image 1">
        </body></html>"""
        actual = extract_page_data(input_body, input_url)
        expected = {
            "url": "https://crawler-test.com",
            "heading": "Test Title",
            "first_paragraph": "This is the first paragraph.",
            "outgoing_links": ["https://crawler-test.com/link1"],
            "image_urls": ["https://crawler-test.com/image1.jpg"],
        }
        self.assertEqual(actual, expected)
    def test_extract_page_data_blank_page(self):
        input_url = "https://crawler-test.com"
        input_body = '<html><body></body></html>'
        actual = extract_page_data(input_body, input_url)
        expected = {
            "url": "https://crawler-test.com",
            "heading": "",
            "first_paragraph": "",
            "outgoing_links": [],
            "image_urls": [],
        }
        self.assertEqual(actual, expected)
    def test_extract_page_data_multiple_links(self):
        input_url = "https://crawler-test.com"
        input_body = """<html><body>
            <a href="/link1">Link 1</a>
            <a href="/link2">Link 2</a>
        </body></html>"""
        actual = extract_page_data(input_body, input_url)
        expected = {
            "url": "https://crawler-test.com",
            "heading": "",
            "first_paragraph": "",
            "outgoing_links": ["https://crawler-test.com/link1", "https://crawler-test.com/link2"],
            "image_urls": [],
        }
        self.assertEqual(actual, expected)
    def test_extract_page_data_multiple_image_urls(self):
        input_url = "https://crawler-test.com"
        input_body = """<html><body>
            <img src="/image1.jpg" alt="Image 1">
            <img src="/image2.jpg" alt="Image 2">
        </body></html>"""
        actual = extract_page_data(input_body, input_url)
        expected = {
            "url": "https://crawler-test.com",
            "heading": "",
            "first_paragraph": "",
            "outgoing_links": [],
            "image_urls": ["https://crawler-test.com/image1.jpg", "https://crawler-test.com/image2.jpg"],
        }
        self.assertEqual(actual, expected)
if __name__ == "__main__":
    unittest.main()
