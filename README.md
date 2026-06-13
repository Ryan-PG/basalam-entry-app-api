# Basalam Entry App (Feedback Board API)

A production-ready RESTful backend API for a Feedback Board system, built with Python 3.12, FastAPI, SQLAlchemy 2.0 (Async), and SQLite. 

> Note that this application also contains a UI in this repo:
> https://github.com/Ryan-PG/basalam-entry-app-ui

---

## 1. Local Setup & Execution Guide

### Prerequisites
* [Docker](https://docs.docker.com/get-docker/) and Docker Compose (Recommended)
* Python 3.12+ (If running without Docker)

### Option A: Running with Docker (Recommended)
The easiest way to get the application running is via Docker. The provided configuration handles the application runtime and database table initialization automatically on startup.

1. **Clone the repository and navigate to the root directory.**
2. **Build and start the container:**
    ```bash
    docker compose up --build
    ```
3. **Access the application:**
    * API Documentation (Swagger UI): http://localhost:8000/docs
    * ReDoc: http://localhost:8000/redoc

> **Note:** The application is configured to automatically inspect your data directory and generate the SQLite database file along with all required tables the exact moment the FastAPI app starts up.

### Option B: Running Locally (Without Docker)

1. **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```
2. **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
3. **Configure environment variables:**
    * The app uses `pydantic-settings` and defaults to development settings. You can create a `.env` file in the root directory to override them:
    ```env
    DATABASE_URL=sqlite+aiosqlite:///./feedback.db
    SECRET_KEY=your_secure_secret_key
    ```
4. **Start the development server:**
    ```bash
    uvicorn app.main:app --reload
    ```
    *The SQLite database file (`feedback.db`) will automatically be generated in your project directory upon launching the server.*

### Running the Test Suite
The project includes a comprehensive Pytest suite that uses an isolated, in-memory SQLite database instance to avoid touching your local data files during evaluation.
```bash
pytest --cov=app tests/

```

---

## 2. Technical Decisions & Architecture

As a senior engineer, my goal was to balance clean architecture principles with maintainability, strictly avoiding over-engineering while ensuring the app is robust enough for production usage.

* **FastAPI over Flask/Django:** FastAPI was chosen for its native async support, exceptionally fast execution metrics, and seamless integration with Pydantic for structural data validation. The automatic OpenAPI documentation generation provides instant, living API specs.
* **Layered "Clean" Architecture:** The codebase explicitly decouples data layers from transport delivery mechanisms:
* **Routers (`app/api/`)**: Strictly handle HTTP requests, routing, status codes, and dependency injection wrappers.
* **Services (`app/services/`)**: Contain all core business logic workflows. This completely decouples domain rules from the web framework layer, making them trivial to unit-test.
* **Repositories (`app/repositories/`)**: Abstract database transactions using the repository pattern. If we ever swap underlying storage strategies, our service layer remains untouched.


* **SQLAlchemy 2.0 with AsyncIO (`aiosqlite`):** I utilized modern SQLAlchemy 2.0 declarative mapping configurations (`Mapped` and `mapped_column`). This provides excellent static typing analysis tools. Combining this with an asynchronous SQLite driver (`aiosqlite`) ensures our network and database I/O operations don't block FastAPI's primary execution loop.
* **Automated SQLite Initialization:** To eliminate deployment friction and avoid unnecessary migration overhead for a self-contained SQLite configuration, the relational layout is built programmatically inside the application lifecycle hooks using `Base.metadata.create_all`.
* **UUID Primary Keys:** Utilizing cryptographically secure UUID identifiers instead of incremental integers prevents end-users from performing sequential resource enumeration attacks.
* **Pydantic V2:** Leveraged for input/output model parsing. V2 is heavily optimized with a core written in Rust, offering massive performance benefits.
* **Multi-stage Docker Build:** The container strategy separates dependencies installation compilation phases from execution processes, decreasing the overall footprint of the production-ready machine image while guaranteeing operations run entirely under a non-privileged system user account (`appuser`).

---

## 3. Application Screenshots

*(Replace the placeholder descriptions below with the actual relative paths to your graphic elements once captured, or host them within a `/docs/images/` repository directory).*

### Main API Documentation (Swagger UI)

Provides an overview of all available endpoints for public users and administrators.


### Feedback Registration Section

The public-facing endpoint and schema where users can submit their feedback (Title and Message).


### Admin Status Dashboard

The protected dashboard/endpoint where authenticated administrators can filter feedbacks and update their status (e.g., to `under_review` or `resolved`).
