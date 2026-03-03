import requests
from bs4 import BeautifulSoup
import csv
import time
import random
import os
import json
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

session = requests.Session()

retries = Retry(
    total=5,
    backoff_factor=2,
    status_forcelist=[429, 500, 502, 503, 504]
)

session.mount("https://", HTTPAdapter(max_retries=retries))

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

BASE_LIST_URL = "https://www.shl.com/products/product-catalog/?type=1&start={}"


def get_product_links():
    results = []
    page = 0

    while True:
        url = BASE_LIST_URL.format(page)
        print("Fetching list:", url)

        try:
            response = session.get(url, headers=HEADERS, timeout=10)
            response.raise_for_status()
        except Exception as e:
            print("⚠ Error fetching list page:", e)
            time.sleep(5)
            continue

        soup = BeautifulSoup(response.text, "lxml")

        links = []
        for a in soup.find_all("a", href=True):
            if "/products/product-catalog/view/" in a["href"]:
                links.append("https://www.shl.com" + a["href"])

        links = list(set(links))
        print("Links found:", len(links))

        if not links:
            break

        results.extend(links)
        page += 12
        time.sleep(2)

    return list(set(results))


def scrape_details(url):
    try:
        response = session.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
    except Exception as e:
        print(f"⚠ Error fetching {url}: {e}")
        time.sleep(5)
        return None

    soup = BeautifulSoup(response.text, "lxml")

    name = soup.find("h1").text.strip() if soup.find("h1") else ""
    description = (
        soup.find("meta", {"name": "description"})["content"]
        if soup.find("meta", {"name": "description"})
        else ""
    )

    duration = ""
    adaptive = ""
    remote = ""
    test_types = []

    for li in soup.find_all("li"):
        text = li.text.strip()

        if "Duration" in text:
            duration = text.replace("Duration", "").strip()

        if "Adaptive" in text:
            adaptive = text.split(":")[-1].strip()

        if "Remote" in text:
            remote = text.split(":")[-1].strip()

        if text in [
            "Knowledge & Skills",
            "Personality & Behavior",
            "Ability & Aptitude",
            "Competencies",
            "Development & 360",
            "Assessment Exercises",
            "Simulations",
            "Biodata & Situational Judgement",
        ]:
            test_types.append(text)

    time.sleep(random.uniform(1.5, 3.5))

    return {
        "name": name,
        "url": url,
        "description": description,
        "duration": duration,
        "adaptive_support": adaptive,
        "remote_support": remote,
        "test_type": ",".join(test_types),
    }


def main():
    links = get_product_links()
    print("Total links:", len(links))

    all_data = []

    for i, link in enumerate(links):
        print(f"[{i+1}/{len(links)}] Scraping:", link)
        data = scrape_details(link)
        if data:
            all_data.append(data)

    # Save CSV
    with open("data/processed/shl_full_catalogue.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=all_data[0].keys())
        writer.writeheader()
        writer.writerows(all_data)

    print("✅ Full metadata scraping complete.")

    # Save RAW JSON
    os.makedirs("data/raw", exist_ok=True)
    with open("data/raw/shl_raw.json", "w", encoding="utf-8") as f:
        json.dump(all_data, f, indent=2)

    print("✅ Stage 1 Complete: Raw data saved.")


if __name__ == "__main__":
    main()