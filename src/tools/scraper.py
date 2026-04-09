import os
import time
import urllib3
from curl_cffi import requests
from bs4 import BeautifulSoup



urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# --- 2. ADD ALL YOUR FULL URL LIST --- YOUR ASSISTANT WILL COLLECT INFO FROM THESE URLS 
URLS = [
    ...,
	...,
	...,
	...,
	....
]

human_headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://www.google.com/",
    "Upgrade-Insecure-Requests": "1"
}

## -----UPDATE THE OUTPUT DIR PATH
OUTPUT_DIR = r"...\PIA_ONPREM\data\raw_docs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def scrape_pubali():
    print("--- Starting PIA Stealth Scraper ---")
    print(f"Targeting {len(URLS)} URLs...")

    # Initialize session with browser impersonation and proxy
    # In curl_cffi, proxies are passed to the Session constructor
    with requests.Session(
        impersonate="chrome110", 
        proxies={"http": BANK_PROXY, "https": BANK_PROXY},
        verify=False,
        timeout=30
    ) as session:
        
        for url in URLS:
            try:
                print(f"\n[Scraping]: {url}")
                
                #response = session.get(url)
                response = session.get(url, headers=human_headers)

                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    
                    # Remove non-content elements to save space in the Vector DB
                    for element in soup(["script", "style", "nav", "footer", "header"]):
                        element.extract()
                    
                    # Extract text and clean up whitespace
                    lines = (line.strip() for line in soup.get_text().splitlines())
                    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
                    clean_text = '\n'.join(chunk for chunk in chunks if chunk)
                    
                    # Create filename from URL slug
                    slug = url.rstrip("/").split("/")[-1]
                    filename = f"{slug}_content.txt"
                    file_path = os.path.join(OUTPUT_DIR, filename)
                    
                    with open(file_path, "w", encoding="utf-8") as f:
                        f.write(f"Source URL: {url}\n\n{clean_text}")
                    
                    print(f"Successfully saved: {filename}")
                else:
                    print(f"Blocked or Missing (Status {response.status_code})")

                # Anti-Bot Protection: Random delay between 2-4 seconds
                time.sleep(2.5)

            except Exception as e:
                print(f"Error connecting to {url}: {e}")

if __name__ == "__main__":
    scrape_pubali()