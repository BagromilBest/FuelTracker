# Fuel Tracker

A web application for tracking fuel consumption, rides, and expenses across multiple users sharing a vehicle.

## Features

- **Multi-user tracking**: Track rides and fuel consumption for multiple drivers
- **Automatic calculations**: Enter any 2 of 3 values (distance, consumption, fuel) and the app calculates the third
- **Tank cycles**: Organize rides into tank cycles (from fill-up to fill-up)
- **Statistics**: View aggregated statistics per user and per cycle
- **Cost tracking**: Monitor fuel costs based on configurable fuel prices
- **History**: Browse past tank cycles and their statistics

## Tech Stack

### Backend
- **FastAPI**: Modern Python web framework
- **SQLAlchemy**: ORM for database interactions
- **SQLite**: Lightweight database for data persistence
- **Pydantic**: Data validation using Python type annotations

### Frontend
- **Vue 3**: Progressive JavaScript framework
- **Vue Router**: Official router for Vue.js
- **Pinia**: State management for Vue
- **Vite**: Fast build tool and dev server
- **Chart.js**: Data visualization
- **Axios**: HTTP client

## Project Structure

```
FuelTracker/
├── backend/
│   ├── app/
│   │   ├── main.py          # FastAPI app with all routes
│   │   ├── database.py      # Database connection setup
│   │   ├── models.py        # SQLAlchemy models
│   │   ├── schemas.py       # Pydantic schemas
│   │   └── logic.py         # Fuel calculation logic
│   ├── Dockerfile           # Production Docker image
│   └── requirements.txt     # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── components/      # Reusable Vue components
│   │   ├── views/           # Page components
│   │   ├── stores/          # Pinia stores
│   │   ├── services/        # API client
│   │   ├── router/          # Vue Router setup
│   │   ├── App.vue          # Root component
│   │   └── main.js          # App entry point
│   ├── Dockerfile           # Production Docker image
│   ├── Dockerfile.dev       # Development Docker image
│   ├── vite.config.js       # Vite configuration
│   ├── index.html           # HTML entry point
│   └── package.json         # Node dependencies
└── docker-compose.yml       # Docker services orchestration
```

## Getting Started

### Prerequisites

- Docker and Docker Compose (recommended)
- OR:
  - Python 3.11+ (for backend)
  - Node.js 18+ (for frontend)

### Running with Docker Compose

1. Clone the repository:
```bash
git clone https://github.com/BagromilBest/FuelTracker.git
cd FuelTracker
```

2. Start the application:
```bash
docker compose up
```

3. Access the application:
   - Frontend: http://localhost:5173
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

### Running Locally (Development)

#### Backend

1. Navigate to the backend directory:
```bash
cd backend
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

4. Run the server:
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### Frontend

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Run the development server:
```bash
npm run dev
```

4. Access the application at http://localhost:5173

### Building for Production

#### Frontend
```bash
cd frontend
npm run build
```

The built files will be in the `dist/` directory.

## API Endpoints

- `GET /api/settings` - Get application settings
- `PUT /api/settings` - Update settings
- `GET /api/users` - List all active users
- `POST /api/users` - Create a new user
- `POST /api/rides` - Log a new ride
- `GET /api/cycles` - List all tank cycles
- `POST /api/cycles/close` - Close current cycle and start a new one
- `GET /api/stats` - Get statistics for current or specific cycle

For detailed API documentation, visit http://localhost:8000/docs when running the backend.

## Usage

### Adding Users

1. Navigate to Settings page
2. Enter user name and pick a color
3. Click "Add User"

### Logging Rides

1. On the Dashboard, select a user
2. Enter at least 2 of the following:
   - Distance (km)
   - Consumption (L/100km)
   - Fuel used (L)
3. The app will calculate the missing value
4. Click "Save Ride"

### Closing Tank Cycles

When you refill the tank, close the current cycle:
1. Click "Refill Tank / Close Cycle" on the Dashboard
2. This creates a new cycle and archives the current one

### Viewing History

Navigate to the History page to:
- See all past tank cycles
- View detailed statistics for each cycle
- Compare consumption across different cycles

### Configuring Settings

Navigate to Settings to:
- Set currency for cost calculations
- Update fuel price per liter
- Manage users

## Database

The application uses SQLite with the following models:

- **Setting**: Application-wide settings (currency, fuel price)
- **User**: Drivers/users who log rides
- **TankCycle**: Periods between fuel refills
- **Ride**: Individual trips with distance, consumption, and fuel data

## License

This project is open source and available under the MIT License.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
