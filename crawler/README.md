# Web Crawler & Phone Extraction

A web crawler using BFS to find and extract phone numbers within a given domain.

## Tech Stack
- `requests` for fetching pages
- `BeautifulSoup` for HTML parsing
- `re` for phone number extraction
- `urllib.parse` for handling domain logic

## Trade-offs and Considerations
- **Why BFS for crawler?** BFS ensures we discover all pages at a lower depth before diving deeper, which tends to yield more relevant results closer to the entry point and is simpler to implement iteratively with a queue. It avoids getting stuck in deep paths.
- **Why Regex for phone extraction?** Phone numbers have very consistent structural patterns globally (digits, spaces, hyphens). Regex is highly efficient compared to using NLP or other heuristics, especially when paired with simple standardization routines.
- **Edge cases handled:** Broken links (caught with exceptions), Infinite Loops (prevented using `visited` set), fragments are ignored.

## Scaling Considerations

- For large-scale crawling:
  - Use async requests (aiohttp) for concurrency
  - Use distributed queues (Kafka/RabbitMQ)
  - Respect robots.txt and rate limiting
  - Store results in a database instead of memory

## Limitations

- Cannot extract numbers from JavaScript-rendered content
- Regex may produce false positives
- No politeness policy (rate limiting)

## How to run
```bash
pip install requests beautifulsoup4
python crawler.py <url>
```

### Output
Extracted phone numbers are printed to the console and automatically saved to `phones.txt` in the root directory for persistence.
