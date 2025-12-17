from playwright.sync_api import sync_playwright, TimeoutError
import json
import time

BASE_URL = "https://www.shl.com/products/product-catalog/"
OUTPUT_FILE = "shl_assessments_real.json"


def infer_test_type(name):
    n = name.lower()
    types = []

    if any(k in n for k in ["numerical", "verbal", "reasoning", "verify"]):
        types.append("Ability & Aptitude")
    if any(k in n for k in ["java", "python", "sql", ".net", "javascript"]):
        types.append("Knowledge & Skills")
    if any(k in n for k in ["personality", "opq", "behavior"]):
        types.append("Personality & Behaviour")
    if any(k in n for k in ["simulation", "scenario"]):
        types.append("Simulations")
    if any(k in n for k in ["manager", "leader", "competency"]):
        types.append("Competencies")

    return types or ["General"]


def infer_duration(types):
    if "Simulations" in types:
        return 75
    if "Knowledge & Skills" in types:
        return 60
    if "Personality & Behaviour" in types:
        return 30
    if "Ability & Aptitude" in types:
        return 25
    return 45


def scrape_shl():
    results = []
    seen = set()
    start = 0
    page_num = 1

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        while True:
            url = f"{BASE_URL}?start={start}&type=2"
            print(f"\n🔎 Scraping page {page_num}: {url}")

            page.goto(url, timeout=60000)

            try:
                page.wait_for_selector(
                    "a[href*='/products/product-catalog/view/']",
                    timeout=15000
                )
            except TimeoutError:
                print("❌ No more assessments found. Stopping.")
                break

            cards = page.locator("a[href*='/products/product-catalog/view/']")
            count = cards.count()

            print(f"Found {count} assessments")

            if count == 0:
                break

            for i in range(count):
                try:
                    card = cards.nth(i)
                    href = card.get_attribute("href")
                    name = card.inner_text().strip()

                    if not href or not name:
                        continue

                    if not href.startswith("http"):
                        href = "https://www.shl.com" + href

                    if href in seen:
                        continue

                    seen.add(href)

                    test_types = infer_test_type(name)

                    results.append({
                        "name": name,
                        "url": href,
                        "description": "SHL assessment measuring ability & aptitude capabilities.",
                        "duration": infer_duration(test_types),
                        "remote_support": "Yes",
                        "adaptive_support": "Yes" if "Ability & Aptitude" in test_types else "No",
                        "test_type": test_types
                    })

                except Exception:
                    continue

            start += 12
            page_num += 1
            time.sleep(2)

        browser.close()

    print(f"\n✅ TOTAL REAL ASSESSMENTS: {len(results)}")

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print(f"✅ Saved to {OUTPUT_FILE}")


if __name__ == "__main__":
    scrape_shl()
