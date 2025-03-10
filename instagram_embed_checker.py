import requests
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET

class InstagramEmbedChecker:
    def __init__(self, sitemap_url):
        self.sitemap_url = sitemap_url
        self.pages_to_scan = set()
        self.broken_pages = set()

        # Patterns of sitemaps to skip
        self.skip_patterns = [
            "/example-1","example-2"
        ]

    def fetch_xml(self, url):
        """ Fetch an XML sitemap and return its parsed root. """
        try:
            response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
            response.raise_for_status()
            return ET.fromstring(response.text)
        except requests.RequestException as e:
            print(f"❌ Failed to fetch XML: {url} | Error: {e}")
            return None

    def should_skip_sitemap(self, url):
        """ Check if the sitemap should be skipped based on its URL. """
        return any(url.startswith(pattern) for pattern in self.skip_patterns)

    def parse_sitemap(self, url):
        """ Recursively parse a sitemap (handling both direct URLs and nested sitemaps). """
        if self.should_skip_sitemap(url):
            print(f"⏭️  Skipping sitemap: {url}")
            return
        
        print(f"Fetching sitemap: {url}")
        root = self.fetch_xml(url)
        if root is None:
            return

        namespace = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}

        for elem in root.findall(".//ns:loc", namespace):
            page_url = elem.text.strip()

            if page_url.endswith(".xml"):  # It's a nested sitemap
                self.parse_sitemap(page_url)
            else:
                self.pages_to_scan.add(page_url)

    def fetch_page(self, url):
        """ Fetch a webpage and return its parsed HTML soup. """
        try:
            response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
            if response.status_code != 200:
                return None
            return BeautifulSoup(response.text, "html.parser")
        except requests.RequestException:
            return None

    def check_instagram_embeds(self, soup, page_url):
        """ Check for broken Instagram embeds on a page. """
        instagram_iframes = soup.find_all("iframe", src=True)

        for iframe in instagram_iframes:
            iframe_url = iframe["src"]
            if "instagram.com" in iframe_url:
                try:
                    iframe_response = requests.get(iframe_url, headers={"User-Agent": "Mozilla/5.0"}, timeout=5)
                    iframe_soup = BeautifulSoup(iframe_response.text, "html.parser")

                    # Look for Instagram's broken embed error message
                    error_message = iframe_soup.find("div", class_="ebmMessage")
                    if error_message and "may be broken" in error_message.text:
                        self.broken_pages.add(page_url)
                        return  # No need to check more, mark page as broken

                except requests.RequestException:
                    self.broken_pages.add(page_url)
                    return

    def scan(self):
        """ Start full website scan using sitemap URLs. """
        self.parse_sitemap(self.sitemap_url)  # Get all real pages

        print(f"\n🔍 Scanning {len(self.pages_to_scan)} pages...\n")

        for page_url in self.pages_to_scan:
            print(f"Scanning: {page_url}")
            soup = self.fetch_page(page_url)
            if not soup:
                continue

            # Check Instagram embeds
            self.check_instagram_embeds(soup, page_url)

        print("\n🔎 Scan Complete!\n")
        if self.broken_pages:
            print("🚨 Pages with Broken Instagram Embeds:")
            for page in self.broken_pages:
                print(f"- {page}")
        else:
            print("✅ No broken Instagram embeds found!")

if __name__ == "__main__":
    sitemap_url = input("Enter the XML Sitemap URL: ").strip()
    scanner = InstagramEmbedChecker(sitemap_url)
    scanner.scan()
