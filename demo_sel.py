import requests
import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

def document_broken_links():
    # 1. Setup Headless Chrome (Fastest for background auditing)
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=options)
    
    target_url = "https://www.fefundinfo.com/"
    print(f"🚀 Scanning {target_url} for broken assets...")

    try:
        driver.get(target_url)
        
        # Extract all links and images
        all_links = driver.find_elements(By.TAG_NAME, "a")
        all_images = driver.find_elements(By.TAG_NAME, "img")

        # 2. Report Headers
        report = []
        report.append("="*60)
        report.append(f"WEBSITE HEALTH AUDIT: {target_url}")
        report.append(f"Report Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("="*60 + "\n")

        broken_found = False

        # 3. Check Links
        report.append("--- [ SECTION: BROKEN LINKS ] ---")
        for link in all_links:
            url = link.get_attribute("href")
            if url and url.startswith("http"):
                try:
                    # 'head' is faster as it doesn't download the full page content
                    resp = requests.head(url, timeout=5, allow_redirects=True)
                    if resp.status_code >= 400:
                        report.append(f"❌ Status {resp.status_code} | Link: {url}")
                        broken_found = True
                except Exception:
                    report.append(f"⚠️ Connection Failed | Link: {url}")
                    broken_found = True

        # 4. Check Images
        report.append("\n--- [ SECTION: BROKEN IMAGES ] ---")
        for img in all_images:
            src = img.get_attribute("src")
            if src and src.startswith("http"):
                try:
                    resp = requests.head(src, timeout=5)
                    if resp.status_code >= 400:
                        report.append(f"❌ Status {resp.status_code} | Image: {src}")
                        broken_found = True
                except Exception:
                    # Some images block 'head' requests; we can try 'get' as a backup if needed
                    pass 

        if not broken_found:
            report.append("\n✅ Result: No broken links or images were detected in this audit.")

        # 5. Write to brokenlink.txt
        with open("brokenlink.txt", "w", encoding="utf-8") as file:
            file.write("\n".join(report))

        print("🏁 Audit Finished! All results saved to 'brokenlink.txt'.")

    except Exception as e:
        print(f"🛑 Error during audit: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    document_broken_links()