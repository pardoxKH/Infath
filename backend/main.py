from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import numpy as np
from model_loader import ModelLoader
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI(
    title="Property Value Prediction API",
    description="API for making property value predictions using a GradientBoostingRegressor model",
    version="1.0.0"
)

# Add CORS middleware with more permissive settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://infath.vercel.app", "https://infath-y6pj.vercel.app"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)


# Initialize model loader
model_loader = ModelLoader(
    model_path="gbm_optuna_model.pkl",
    target_scaler_path="target_scaler.pkl",
    standard_scaler_path="standard_scaler.pkl"
)

class PropertyInput(BaseModel):
    Area: float
    AssetLevelId: str
    East_order: str
    EvaluationAssetTypeName: str
    Latitude: float
    LengthFromEast: float
    LengthFromNorth: float
    LengthFromSouth: float
    LengthFromWest: float
    Longitude: float
    NorthBorder: str
    PropAssetCityName: str
    PropAssetNeighborhoodName: str
    PropAssetRegionName: str
    SouthBorder: str
    StreetWidth: float
    WestBorder: str

@app.get("/")
async def root():
    """Health check endpoint"""
    return {"status": "healthy", "message": "Property Value Prediction API is running"}

@app.post("/predict")
async def predict(property_input: PropertyInput):
    """
    Make predictions using the GradientBoostingRegressor model
    
    Args:
        property_input (PropertyInput): Input features for prediction
        
    Returns:
        dict: Model prediction
    """
    try:
        # Convert input to dictionary
        input_dict = property_input.dict()
        
        # Make prediction
        prediction, _ = model_loader.predict(input_dict)
        
        print(f"API prediction: {prediction}")
        return {"prediction": prediction}
    except Exception as e:
        print(f"API error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 