"""
Wix Site Scraper for digital-finance-msca.com/blockchain
Uses Playwright to render JavaScript and extract content.
"""

import json
import os
import re
import time
from pathlib import Path
from urllib.parse import urljoin, urlparse

try:
    from playwright.sync_api import sync_playwright
except ImportError:
    print("Installing playwright...")
    os.system("pip install playwright")
    os.system("playwright install chromium")
    from playwright.sync_api import sync_playwright

import requests


def download_file(url: str, save_path: Path) -> bool:
    """Download a file from URL to the specified path."""
    try:
        response = requests.get(url, timeout=30, stream=True)
        response.raise_for_status()
        save_path.parent.mkdir(parents=True, exist_ok=True)
        with open(save_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"Downloaded: {save_path.name}")
        return True
    except Exception as e:
        print(f"Failed to download {url}: {e}")
        return False


def scrape_blockchain_page(output_dir: Path) -> dict:
    """Scrape the blockchain page and extract all content."""

    url = "https://www.digital-finance-msca.com/blockchain"
    content = {
        "url": url,
        "title": "",
        "sections": [],
        "images": [],
        "downloads": [],
        "links": []
    }

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        print(f"Loading {url}...")
        page.goto(url, wait_until="networkidle", timeout=60000)

        # Wait for content to render
        time.sleep(3)

        # Get page title
        content["title"] = page.title()
        print(f"Page title: {content['title']}")

        # Extract all text content
        text_elements = page.query_selector_all("h1, h2, h3, h4, h5, h6, p, span, div")
        seen_texts = set()

        for elem in text_elements:
            try:
                text = elem.inner_text().strip()
                if text and len(text) > 10 and text not in seen_texts:
                    seen_texts.add(text)
                    tag = elem.evaluate("el => el.tagName.toLowerCase()")
                    content["sections"].append({
                        "tag": tag,
                        "text": text
                    })
            except:
                pass

        # Extract images
        images = page.query_selector_all("img")
        images_dir = output_dir / "assets" / "images"
        images_dir.mkdir(parents=True, exist_ok=True)

        for i, img in enumerate(images):
            try:
                src = img.get_attribute("src")
                alt = img.get_attribute("alt") or f"image_{i}"
                if src and not src.startswith("data:"):
                    full_url = urljoin(url, src)
                    ext = Path(urlparse(src).path).suffix or ".png"
                    filename = re.sub(r'[^\w\-]', '_', alt)[:50] + ext

                    content["images"].append({
                        "src": full_url,
                        "alt": alt,
                        "local": f"assets/images/{filename}"
                    })
                    download_file(full_url, images_dir / filename)
            except:
                pass

        # Extract PDF and downloadable links
        links = page.query_selector_all("a[href]")
        downloads_dir = output_dir / "assets" / "downloads"
        downloads_dir.mkdir(parents=True, exist_ok=True)

        for link in links:
            try:
                href = link.get_attribute("href")
                text = link.inner_text().strip()

                if href:
                    full_url = urljoin(url, href)

                    # Check for downloadable files
                    if any(ext in href.lower() for ext in ['.pdf', '.xlsx', '.csv', '.zip', '.docx']):
                        filename = Path(urlparse(href).path).name
                        content["downloads"].append({
                            "url": full_url,
                            "text": text,
                            "local": f"assets/downloads/{filename}"
                        })
                        download_file(full_url, downloads_dir / filename)
                    else:
                        content["links"].append({
                            "url": full_url,
                            "text": text
                        })
            except:
                pass

        # Take a screenshot
        screenshots_dir = output_dir / "screenshots"
        screenshots_dir.mkdir(parents=True, exist_ok=True)
        page.screenshot(path=str(screenshots_dir / "blockchain_page.png"), full_page=True)
        print("Screenshot saved")

        browser.close()

    # Save content as JSON
    with open(output_dir / "scraped_content.json", "w", encoding="utf-8") as f:
        json.dump(content, f, indent=2, ensure_ascii=False)

    print(f"\nScraped content saved to {output_dir / 'scraped_content.json'}")
    print(f"Sections found: {len(content['sections'])}")
    print(f"Images found: {len(content['images'])}")
    print(f"Downloads found: {len(content['downloads'])}")

    return content


if __name__ == "__main__":
    script_dir = Path(__file__).parent
    output_dir = script_dir

    print("Starting Wix site scraper...")
    print("=" * 50)

    content = scrape_blockchain_page(output_dir)

    print("=" * 50)
    print("Scraping complete!")
