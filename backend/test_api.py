import requests
import json

url = "http://localhost:8000/predict"
payload = {
    "PropAssetNeighborhoodName": "حي الشفا",
    "PropAssetCityName": "Riyadh",
    "Area": 500.0,
    "LengthFromNorth": 20.0,
    "LengthFromSouth": 20.0,
    "LengthFromEast": 25.0,
    "LengthFromWest": 25.0,
    "NorthBorder": "شارع الرئيسي",
    "SouthBorder": "مبنى تجاري",
    "East_order": "قطعة ارض",
    "WestBorder": "حديقة عامة",
    "StreetWidth": 15.0,
    "Latitude": 24.7136,
    "Longitude": 46.6753,
    "PropAssetRegionName": "Riyadh",
    "EvaluationAssetTypeName": "Housing Land",
    "AssetLevelId": "A"
}

response = requests.post(url, json=payload)
print(response.json())