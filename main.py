import sys

import crawl


def main():
    url = sys.argv[1]
    page_data = crawl.crawl_page(url)
    if page_data:
        print(page_data)
    if len(sys.argv) < 2:
        print("no website provided")
        sys.exit(1)
    if len(sys.argv) > 2:
        print("too many arguments provided")
        sys.exit(1)
    print("Hello from web-crawler-in-python!")
    print("Script name:", sys.argv[0])  # example.py
    print("Argument:", sys.argv[1])  # -v
    base_url = sys.argv[1]
    print(f"starting crawl of: {base_url}")
    #When crawl_page() completes, print some information about the collected data to the console - like the number of pages found and iterate over the dictionary values to show the data.


    print(f"Found {len(page_data)} pages:")
    for page in page_data.values():
        print(f"- {page['url']}:\n {len(page['outgoing_links'])} outgoing links\n")


if __name__ == "__main__":
    main()
