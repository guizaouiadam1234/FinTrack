# 💰 FinTrack

A full-stack personal finance tracking application that helps you manage and monitor your transactions with ease.

## 🛠️ Tech Stack

| Layer     | Technology                          |
|-----------|-------------------------------------|
| Frontend  | Vue 3, Vite, Tailwind CSS, Axios    |
| Backend   | Python, FastAPI, SQLAlchemy         |
| Testing   | Vitest (frontend), Pytest (backend) |

## 📁 Project Structure

```
FinTrack/
├── frontend/         # Vue 3 SPA
│   ├── src/
│   ├── tests/
│   └── ...
└── backend/          # FastAPI REST API
    ├── app/
    │   ├── models/
    │   ├── routers/
    │   └── services/
    ├── tests/
    └── main.py
```

## 🚀 Getting Started

### Prerequisites

- Node.js (v18+)
- Python (3.10+)

### Backend Setup

```bash
cd backend

# Create and activate a virtual environment
python -m venv ../.venv
# On Windows:
../.venv/Scripts/activate
# On macOS/Linux:
source ../.venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the development server
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`.

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Run the development server
npm run dev
```

The app will be available at `http://localhost:5173`.

## 🧪 Testing

### Backend

```bash
cd backend

# Run all tests
make test

# Run unit tests only
make test-unit

# Run integration tests only
make test-integration

# Generate HTML coverage report
make test-cov-html
```

### Frontend

```bash
cd frontend

# Run all tests with coverage
npm test

# Run unit tests only
npm run test:unit

# Run integration tests only
npm run test:integration

# Generate HTML coverage report
npm run test:cov-html
```

## 📡 API Overview

| Method | Endpoint       | Description              |
|--------|----------------|--------------------------|
| GET    | `/`            | Health check             |
| POST   | `/auth`        | Authentication           |
| *      | `/transactions`| Transaction Management   |

# 🤝 Contributing
- Fork the repository
- Create a feature branch: `git checkout -b feature/my-feature`
- Commit your changes: `git commit -m 'Add my feature'`
- Push to the branch: `git push origin feature/my-feature`
- Open a Pull Request
