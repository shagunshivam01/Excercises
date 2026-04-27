import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urldefrag
from collections import deque
import logging

from utils import is_same_domain, extract_phone_numbers

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def crawl_for_phones(start_url, max_depth=2, max_pages=50):
    if not start_url.startswith('http'):
        start_url = 'https://' + start_url

    queue = deque([(start_url, 0)])
    visited = set()
    seen = {start_url}
    phone_numbers = set()
    pages_crawled = 0
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
    }
    
    while queue:
        current_url, depth = queue.popleft()
        
        if current_url in visited or depth > max_depth:
            continue
            
        if pages_crawled >= max_pages:
            break
            
        logging.info(f"Crawling (Depth {depth}): {current_url}")
        visited.add(current_url)
        
        try:
            response = requests.get(current_url, headers=headers, timeout=5)
            # Skip non-HTML content
            if 'text/html' not in response.headers.get('Content-Type', ''):
                continue
                
            html = response.text
            soup = BeautifulSoup(html, 'html.parser')
            
            # Extract numbers from text
            page_text = soup.get_text(separator=' ')
            new_numbers = extract_phone_numbers(page_text)
            phone_numbers.update(new_numbers)
            
            # If not at max depth, find more links
            if depth < max_depth:
                for a_tag in soup.find_all("a", href=True):
                    href = a_tag['href']
                    
                    # Normalize URL and remove fragments
                    full_url = urljoin(current_url, href)
                    full_url, _ = urldefrag(full_url)
                    
                    if is_same_domain(start_url, full_url) and full_url not in seen:
                        seen.add(full_url)
                        queue.append((full_url, depth + 1))
                        
            pages_crawled += 1
                        
        except requests.RequestException as e:
            logging.error(f"Failed to fetch {current_url}: {e}")
            
    return list(phone_numbers)

if __name__ == "__main__":
    import sys
    test_url = sys.argv[1] if len(sys.argv) > 1 else input("Enter an initial URL to crawl: ").strip()
    if test_url:
        print("Starting crawl...")
        results = crawl_for_phones(test_url, max_depth=2)
        print("\n--- Extracted Phone Numbers ---")
        for num in results:
            print(num)
        
        # Persistence: Save to a file
        with open("phones.txt", "w") as f:
            for num in results:
                f.write(num + "\n")
        print(f"\n✅ Results saved to phones.txt ({len(results)} numbers)")
