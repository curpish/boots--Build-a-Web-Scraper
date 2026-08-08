import sys

def main():
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

if __name__ == "__main__":
    main()
