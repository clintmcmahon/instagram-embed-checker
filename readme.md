# Instagram Embed Checker

A Python script to scan a website for broken Instagram embeds using its XML sitemap. This tool is useful for web admins, developers, and SEO professionals to detect and fix broken Instagram embeds that might impact user experience.

## Features

- Parses an XML sitemap to identify all website pages.
- Scans each page for embedded Instagram iframes.
- Detects broken Instagram embeds by analyzing the embed response.
- Supports skipping specific sitemap patterns.
- Outputs a list of pages with broken Instagram embeds.

## Requirements

Ensure you have **Python 3.7+** installed. The script also requires the following Python packages:

- `requests` (for making HTTP requests)
- `beautifulsoup4` (for parsing HTML)

### Install Dependencies

Use `pip` to install the required packages:

```sh
pip install requests beautifulsoup4
```

## Usage

1. **Download the script**

   Clone the repository or download `instagram_embed_checker.py`:

   ```sh
   git clone https://github.com/clintmcmahon/instagram-embed-checker.git
   cd instagram-embed-checker
   ```

2. **Run the script**

   Execute the script and enter the XML sitemap URL when prompted:

   ```sh
   python instagram_embed_checker.py
   ```

   Or pass the sitemap URL as an argument:

   ```sh
   python instagram_embed_checker.py https://example.com/sitemap.xml
   ```

3. **Review the output**

   The script will print:

   - The number of pages scanned.
   - Any pages found with broken Instagram embeds.

## Example Output

```sh
🔍 Scanning 150 pages...
Scanning: https://example.com/blog-post-1
Scanning: https://example.com/blog-post-2

🚨 Pages with Broken Instagram Embeds:
- https://example.com/blog-post-2

✅ Scan complete!
```

## Configuration

### Skipping Specific Sitemaps

If your sitemap contains URLs that you do not want to scan (e.g., directories that do not contain relevant content), you can modify the `self.skip_patterns` list inside `instagram_embed_checker.py`. This list contains patterns of sitemap URLs that will be ignored.

## License

This project is licensed under the MIT License.

## Contributing

Feel free to submit issues or pull requests to improve this tool!

## Author

Developed by [Clint McMahon](https://github.com/clintmcmahon).

---

Happy scanning! 🚀

