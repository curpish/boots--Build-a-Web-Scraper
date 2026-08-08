import unittest

from crawl import (
    get_first_paragraph_from_html,
    get_heading_from_html,
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
        #hello bear, did you see this?
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
if __name__ == "__main__":
    unittest.main()
