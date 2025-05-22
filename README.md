# Property Valuation API

A FastAPI-based property valuation system for Saudi Arabia, featuring a GradientBoostingRegressor model and a modern Next.js frontend.

## Features

- Property value prediction using machine learning
- Comprehensive feature engineering
- Input validation
- Standardized preprocessing pipeline
- Modern Arabic UI with English number formatting
- Real-time predictions

## Project Structure

```
.
├── backend/
│   ├── main.py              # FastAPI server
│   ├── model_loader.py      # Model loading and prediction
│   ├── preprocessing.py     # Feature preprocessing
│   └── requirements.txt     # Python dependencies
├── frontend/
│   ├── components/          # React components
│   ├── pages/              # Next.js pages
│   ├── public/             # Static assets
│   ├── styles/             # CSS styles
│   └── package.json        # Node.js dependencies
└── README.md
```

## Setup

### Backend

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
cd backend
pip install -r requirements.txt
```

3. Start the server:
```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

### Frontend

1. Install dependencies:
```bash
cd frontend
npm install
```

2. Start the development server:
```bash
npm run dev
```

The frontend will be available at `http://localhost:3000`

## API Endpoints

- `GET /`: Health check endpoint
- `POST /predict`: Make property value predictions

## Model Details

The system uses a GradientBoostingRegressor model trained on Saudi Arabian property data. Features include:
- Property area and dimensions
- Location coordinates
- Property type and level
- Border information
- Street width
- Distance from city center

## License

MIT 