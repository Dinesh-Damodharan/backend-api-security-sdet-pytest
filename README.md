
# Backend API Reliability Tests

Backend API testing framework built with Python and Pytest, focused on validating
system behavior under real-world failure conditions rather than just happy paths.

The project tests reliability, security boundaries, idempotency, concurrency,
observability, and resilience using a FastAPI backend designed to simulate
production-like failure scenarios.

## What This Tests

- Authentication and authorization flows (including BOLA prevention)
- Safe retries using idempotency keys
- Concurrency behavior and state invariants
- Correlation ID propagation for observability
- System recovery under transient failures

## Test Areas
tests/
├── smoke/ # Basic service health
├── securityflows/ # Auth, authz, BOLA
├── abuse/ # Replay, concurrency, invariants
├── observability/ # Correlation ID tracing
├── resilience/ # Chaos and retry behavior


## Tech Stack

- Python
- Pytest
- Requests
- FastAPI (API under test)

## Running the Project

Install dependencies
pip install -r requirements.txt

Start the API
uvicorn app.main:app --reload

Run the tests
pytest







