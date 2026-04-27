# URL Shortener

A fast, scalable URL shortener using Flask and SQLite with Base62 encoding.

## Structure
- `app.py` - Flask API endpoints
- `service.py` - Business logic and Base62 encoding
- `db.py` - Database setup and connections

## Key Design Points

### Idempotency
- Enforced using `UNIQUE(long_url)`.
- The same long URL will consistently return the same short code without duplicates.

### Collision Handling
- Avoided via auto-increment IDs. No hashing means no collision scenarios.
- The auto-increment ID naturally maintains uniqueness.

### Scalability (1M URLs)
- SQLite comfortably handles scales of ~1M URLs for conceptual demonstration and prototyping.
- O(1) time complexity for reads via database direct lookup.

### Production Readiness
For a true production environment serving higher loads, we would:
- Move from SQLite to a distributed relational database like **PostgreSQL**.
- Add **Redis** cache for hot URLs in-memory to drastically decrease read latencies.

## API Design Choices

- POST `/shorten` is idempotent: same input URL always returns the same short URL.
- GET `/{shortCode}` performs a constant-time lookup using indexed database queries.

## Limitations

- No authentication or rate limiting
- No expiration support for URLs
- SQLite is not suitable for high write concurrency

## Future Improvements

- Add Redis caching for hot URLs
- Support custom aliases
- Introduce analytics (click tracking)
- Use consistent hashing for distributed systems

## How to Test
1. Make sure to have `flask` installed (`pip install flask`).
2. Run the server:
   ```bash
   python app.py
   ```
3. Issue a shorten request:
   ```bash
   curl -X POST http://localhost:5000/shorten -H "Content-Type: application/json" -d '{"url": "https://google.com"}'
   ```
4. Access the short link locally:
   ```bash
   http://localhost:5000/<short_code>
   ```
