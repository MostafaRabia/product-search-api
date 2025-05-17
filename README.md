# Product Search API

A high-performance Django REST Framework API for product search with advanced features including trigram similarity search, caching, and rate limiting.

## Features

- Hybrid search functionality combining:
  - Trigram similarity search for typo tolerance
  - Case-insensitive contains search
  - Full-text search capabilities
- Response caching (2 minutes)
- Rate limiting for both authenticated and anonymous users
- Pagination support
- Comprehensive search across multiple fields (name, brand, category, nutrition facts)

## Prerequisites

- Python 3.8+
- PostgreSQL 12+ with pg_trgm extension
- Django 4.0+
- Django REST Framework

## Setup Instructions

1. Clone the repository:
```bash
git clone <repository-url>
cd <repository-name>
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure PostgreSQL:
   - Create a new database
   - Enable the pg_trgm extension:
   ```sql
   CREATE EXTENSION IF NOT EXISTS pg_trgm;
   ```

5. Configure environment variables:
   Create a `.env` file in the project root:
   ```
   cp .env.example .env
   ```

6. Run migrations:
```bash
python manage.py migrate
```

7. Start the development server:
```bash
python manage.py runserver
```

## API Documentation

### Products Endpoint

Base URL: `/api/products/`

#### List/Search Products

**GET** `/api/products/`

Query Parameters:
- `search` (optional): Search query string
- `page` (optional): Page number for pagination
- `page_size` (optional): Number of items per page

Example Request:
```
GET /api/products/?search=organic&page=1&page_size=10
```

Response:
```json
{
    "count": 100,
    "next": "http://api/products/?search=organic&page=2&page_size=10",
    "previous": null,
    "results": [
        {
            "id": 1,
            "name": "Organic Apples",
            "brand": "Fresh Farms",
            "category": "Fruits",
            "nutrition_facts": {
                "calories": 95,
                "protein": 0.5,
                "fiber": 4.5
            }
        },
        // ... more products
    ]
}
```

#### Search Behavior

The API implements a hybrid search strategy:

1. For queries longer than 5 characters:
   - First attempts trigram similarity search (for typo tolerance)
   - Falls back to case-insensitive contains search if no results found

2. For queries 5 characters or shorter:
   - Uses case-insensitive contains search across all fields

#### Rate Limiting

- Authenticated users: 20 requests per minute
- Anonymous users: 10 requests per minute

#### Caching

- List/search results are cached for 2 minutes
- Cache is automatically invalidated when data changes

## Development

### Running Tests

```bash
python manage.py test
```

### Code Style

The project follows PEP 8 guidelines. To check code style:

```bash
flake8
```
