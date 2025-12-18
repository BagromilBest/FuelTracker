# Development Guide

## Local Development Setup

### Prerequisites
- Python 3.14+
- Node.js 18+
- npm or yarn

### Backend Setup

1. Create and activate virtual environment:
```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Start the backend server:
```bash
python -m uvicorn app.main:app --reload --port 8000
```

The backend will be available at `http://localhost:8000`

### Frontend Setup

1. Install dependencies:
```bash
cd frontend
npm install
```

2. Start the development server:
```bash
npm run dev
```

The frontend will be available at `http://localhost:5173`

**Note:** The frontend is automatically configured to proxy API requests to `http://localhost:8000` in local development.

## Docker Development Setup

1. Build and start all services:
```bash
docker-compose up --build
```

2. Access the application:
- Frontend: `http://localhost:5173`
- Backend API: `http://localhost:8000`

**Note:** In Docker, the frontend automatically proxies to `http://backend:8000` (the Docker service name).

## Environment Variables

### Frontend

The frontend uses `VITE_BACKEND_URL` to determine the backend API endpoint:

- **Local Development:** Defaults to `http://localhost:8000` (no configuration needed)
- **Docker:** Automatically set to `http://backend:8000` in `docker-compose.yml`
- **Custom:** Create a `.env` file in the frontend directory:
  ```
  VITE_BACKEND_URL=http://your-backend-url:8000
  ```

### Backend

Backend environment variables can be configured in:
- Local: `.env` file in `backend/` directory
- Docker: `environment` section in `docker-compose.yml`

## Project Structure

```
FuelTracker/
├── backend/
│   ├── app/
│   │   ├── main.py          # FastAPI application
│   │   ├── models.py        # Database models
│   │   ├── schemas.py       # Pydantic schemas
│   │   └── database.py      # Database configuration
│   ├── requirements.txt     # Python dependencies
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── views/           # Vue pages
│   │   ├── components/      # Vue components
│   │   └── stores/          # Pinia stores
│   ├── vite.config.js       # Vite configuration
│   ├── package.json
│   └── Dockerfile.dev
└── docker-compose.yml
```

## API Documentation

Once the backend is running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Troubleshooting

### Backend won't start
- Ensure Python 3.14+ is installed
- Check if port 8000 is available
- Verify all dependencies are installed: `pip install -r requirements.txt`

### Frontend can't connect to backend
- Verify backend is running on port 8000
- Check browser console for errors
- For local dev, backend should be at `http://localhost:8000`
- For Docker, ensure both containers are on the same network

### Hot reload not working in Docker
- Volumes are configured for hot reload
- If issues persist, restart the containers: `docker-compose restart`

## Testing

### Backend Tests
```bash
cd backend
pytest
```

### Frontend Tests
```bash
cd frontend
npm run test
```

## Building for Production

### Backend
```bash
cd backend
docker build -t fueltracker-backend .
```

### Frontend
```bash
cd frontend
npm run build
```

The production build will be in `frontend/dist/`
