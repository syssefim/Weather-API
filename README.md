# Weather API
This project is a custom Weather API built with Flask that fetches and returns weather data from a 3rd-party service. It demonstrates how to integrate external APIs, implement in-memory caching, and manage environment variables securely.

## 🚀 Features
- **External API Integration:** Fetches real-time weather data from Visual Crossing's Timeline API.
- **Redis Caching:** Implements an in-memory Redis cache to store weather data for 30 minutes (1800 seconds). This prevents redundant network calls to the 3rd-party API, speeds up response times, and automatically cleans up old data.
- **Rate Limiting:** Protects the API from abuse using Flask-Limiter. Global limits are set to 200 requests per day and 50 per hour per IP address.
- **Robust Error Handling:** Gracefully catches and handles network connection issues, timeouts, and JSON parsing errors so the application doesn't crash.

## 🛠️ Tech Stack
- **Language:** Python
- **Framework:** Flask
- **HTTP Client:** requests
- **Caching:** Redis
- **Rate Limiting:** Flask-Limiter
- **Environment Management:** python-dotenv




