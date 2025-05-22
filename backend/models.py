from pydantic import BaseModel, Field, validator
from typing import Optional
import re
import pandas as pd

# Load city data from city_center_coords.csv
city_data = pd.read_csv('city_center_coords.csv')
valid_cities = city_data['City_en'].tolist()

# Create a mapping of cities to their regions
city_region_map = dict(zip(city_data['City_en'], city_data['Region']))

# Load region capitals
region_capitals = pd.read_csv('Regions_capitals.csv')
region_capital_map = dict(zip(region_capitals['Region'], region_capitals['Capital']))

class PredictionInput(BaseModel):
    """
    Model for prediction input with feature validation.
    """
    PropAssetNeighborhoodName: str = Field(..., min_length=1, description="Name of the neighborhood")
    PropAssetRegionName: str = Field(..., description="Region name")
    PropAssetCityName: str = Field(..., min_length=1, description="Name of the city")
    Area: float = Field(..., gt=0, description="Area of the property")
    LengthFromNorth: float = Field(..., ge=0, description="Length from north border")
    LengthFromSouth: float = Field(..., ge=0, description="Length from south border")
    LengthFromEast: float = Field(..., ge=0, description="Length from east border")
    LengthFromWest: float = Field(..., ge=0, description="Length from west border")
    NorthBorder: str = Field(..., min_length=1, description="North border description")
    SouthBorder: str = Field(..., min_length=1, description="South border description")
    East_order: str = Field(..., min_length=1, description="East border description")
    WestBorder: str = Field(..., min_length=1, description="West border description")
    StreetWidth: float = Field(..., ge=0, description="Width of the street")
    Latitude: float = Field(..., ge=-90, le=90, description="Latitude coordinate")
    Longitude: float = Field(..., ge=-180, le=180, description="Longitude coordinate")
    EvaluationAssetTypeName: str = Field(..., description="Asset type")
    AssetLevelId: str = Field(..., description="Asset level")

    @validator('PropAssetCityName')
    def validate_city(cls, v, values):
        """Validate that the city exists in our database or use region capital as fallback"""
        if v not in valid_cities:
            # If city not found, try to use region capital
            if 'PropAssetRegionName' in values:
                region = values['PropAssetRegionName']
                capital = region_capital_map.get(region)
                if capital and capital in valid_cities:
                    print(f"City '{v}' not found. Using region capital '{capital}' instead.")
                    return capital
                else:
                    raise ValueError(f'City {v} not found and no valid capital found for region {region}')
            else:
                # If region is not in values yet, we need to validate it first
                raise ValueError(f'City {v} not found. Please provide a valid region first.')
        return v

    @validator('PropAssetRegionName', pre=True)
    def validate_region(cls, v, values):
        """Validate property asset region and ensure it matches the city"""
        valid_regions = [
            "Riyadh",
            "Makkah",
            "Madinah",
            "Eastern Province",
            "Asir",
            "Tabuk",
            "Hail",
            "Northern Borders",
            "Jazan",
            "Najran",
            "Al Baha",
            "Al Jawf",
            "Al Qassim"
        ]
        if v not in valid_regions:
            raise ValueError(f'PropAssetRegionName must be one of: {", ".join(valid_regions)}')
        
        # Check if city is provided and validate city-region match
        if 'PropAssetCityName' in values:
            city = values['PropAssetCityName']
            expected_region = city_region_map.get(city)
            if expected_region != v:
                raise ValueError(f'City {city} belongs to region {expected_region}, but {v} was provided')
        
        return v

    @validator('PropAssetNeighborhoodName', 'NorthBorder', 'SouthBorder', 'East_order', 'WestBorder')
    def validate_string_fields(cls, v):
        """Validate string fields to ensure they don't contain only whitespace or special characters"""
        if not v.strip():
            raise ValueError("Field cannot be empty or contain only whitespace")
        if not re.match(r'^[\u0600-\u06FF\u0750-\u077Fa-zA-Z0-9\s\-\.]+$', v):
            raise ValueError("Field can only contain Arabic letters, English letters, numbers, spaces, hyphens, and periods")
        return v.strip()

    @validator('Area', 'LengthFromNorth', 'LengthFromSouth', 'LengthFromEast', 'LengthFromWest', 'StreetWidth')
    def validate_positive_numbers(cls, v):
        """Validate that numeric fields are positive"""
        if v <= 0:
            raise ValueError("Value must be greater than 0")
        return round(v, 2)  # Round to 2 decimal places

    @validator('Latitude', 'Longitude')
    def validate_coordinates(cls, v):
        """Validate coordinate values"""
        return round(v, 6)  # Round to 6 decimal places for coordinates

    @validator('AssetLevelId')
    def validate_asset_level(cls, v):
        """Validate asset level"""
        valid_levels = ['A', 'B', 'C', 'D']
        if v not in valid_levels:
            raise ValueError(f'AssetLevelId must be one of: {", ".join(valid_levels)}')
        return v

    @validator('EvaluationAssetTypeName')
    def validate_asset_type(cls, v):
        """Validate evaluation asset type"""
        valid_types = [
            "Housing Land",
            "Commercial Land",
            "Raw Land",
            "Farming Land"
        ]
        if v not in valid_types:
            raise ValueError(f'EvaluationAssetTypeName must be one of: {", ".join(valid_types)}')
        return v

    class Config:
        json_schema_extra = {
            "example": {
    "PropAssetNeighborhoodName": "العزيزية",
    "PropAssetCityName": "Madinah",
    "Area": 1050.0,
    "LengthFromNorth": 38.45,
    "LengthFromSouth": 28.46,
    "LengthFromEast": 30.14,
    "LengthFromWest": 30.13,
    "NorthBorder": "قطعة رقم بدون",
    "SouthBorder": "قطعة رقم 162وشارع عرض 12 م",
    "East_order": "قطعة رقم 615",
    "WestBorder": "قطعة رقم 163",
    "StreetWidth": 12.0,
    "Latitude": 24.32,
    "Longitude": 39.25,
    "PropAssetRegionName": "Madinah",
    "EvaluationAssetTypeName": "Housing Land",
    "AssetLevelId": "C"
}
        }

class PredictionResponse(BaseModel):
    """
    Model for prediction response.
    """
    prediction: float 