import numpy as np
import pandas as pd
from typing import Dict, Any, List
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from pydantic import BaseModel, Field, validator
from enum import Enum
import pickle

class FeaturePreprocessor:
    def __init__(self):
        """
        Initialize the feature preprocessor.
        This will be extended with specific preprocessing steps.
        """
        self.categorical_columns = [
            'PropAssetCityName',
            'PropAssetRegionName',
            'EvaluationAssetTypeName',
            'NorthBorder_Type',
            'SouthBorder_Type',
            'East_order_Type',
            'WestBorder_Type',
            'AssetLevelId'
        ]
        
        self.numeric_columns = [
            'Area',
            'LengthFromNorth',
            'LengthFromSouth',
            'LengthFromEast',
            'LengthFromWest',
            'StreetWidth',
            'Latitude',
            'Longitude',
            'Perimeter',
            'Street_Frontage',
            'Num_Street_Fronts'
        ]
        
        # Initialize encoders with known categories
        self.encoders = {}
        
        # Initialize and fit AssetLevelId encoder
        asset_level_encoder = OneHotEncoder(sparse_output=False, handle_unknown='ignore')
        asset_level_encoder.fit(pd.DataFrame({'AssetLevelId': ['A', 'B', 'C', 'D']}))
        self.encoders['AssetLevelId'] = asset_level_encoder
        
        # Initialize and fit EvaluationAssetTypeName encoder
        asset_type_encoder = OneHotEncoder(sparse_output=False, handle_unknown='ignore')
        asset_type_encoder.fit(pd.DataFrame({'EvaluationAssetTypeName': [
            'Housing Land', 'Commercial Land', 'Raw Land', 'Farming Land'
        ]}))
        self.encoders['EvaluationAssetTypeName'] = asset_type_encoder


        # Initialize and fit Border_typ encoder
        NorthBorder_Type_encoder = OneHotEncoder(sparse_output=False, handle_unknown='ignore')
        NorthBorder_Type_encoder.fit(pd.DataFrame({'NorthBorder_Type': [
            'Street', 'Building', 'Empty_Plot', 'Alley', 'Parking', 'Public_space','Other'
        ]}))
        self.encoders['NorthBorder_Type'] = NorthBorder_Type_encoder

        SouthBorder_Type_encoder = OneHotEncoder(sparse_output=False, handle_unknown='ignore')
        SouthBorder_Type_encoder.fit(pd.DataFrame({'SouthBorder_Type': [
            'Street', 'Building', 'Empty_Plot', 'Alley', 'Parking', 'Public_space', 'Other'
        ]}))
        self.encoders['SouthBorder_Type'] = SouthBorder_Type_encoder

        East_order_Type_encoder = OneHotEncoder(sparse_output=False, handle_unknown='ignore')
        East_order_Type_encoder.fit(pd.DataFrame({'East_order_Type': [
            'Street', 'Building', 'Empty_Plot', 'Alley', 'Parking', 'Public_space', 'Other'
        ]}))
        self.encoders['East_order_Type'] = East_order_Type_encoder

        WestBorder_Type_encoder = OneHotEncoder(sparse_output=False, handle_unknown='ignore')
        WestBorder_Type_encoder.fit(pd.DataFrame({'WestBorder_Type': [
            'Street', 'Building', 'Empty_Plot', 'Alley', 'Parking', 'Public_space', 'Other'
        ]}))
        self.encoders['WestBorder_Type'] = WestBorder_Type_encoder


        # Initialize and fit PropAssetRegionName encoder
        region_encoder = OneHotEncoder(sparse_output=False, handle_unknown='ignore')
        region_encoder.fit(pd.DataFrame({'PropAssetRegionName': [
            'Riyadh', 'Makkah', 'Madinah', 'Eastern Province', 
            'Asir', 'Tabuk', 'Hail', 'Northern Borders', 
            'Jazan', 'Najran', 'Bahah', 'Jawf', 'Qassim'
        ]}))
        self.encoders['PropAssetRegionName'] = region_encoder
        
        # Load the pre-trained scaler
        with open('standard_scaler.pkl', 'rb') as f:
            self.scaler = pickle.load(f)
        
        # Load city center coordinates
        self.city_centers = pd.read_csv('city_center_coords.csv')
        self.city_centers = self.city_centers.rename(columns={
            'Latitude': 'City_Center_Lat',
            'Longitude': 'City_Center_Lon'
        })
        
        # Load encoded neighborhood/city values
        self.encoded_neighb_city = pd.read_csv('encoded_neighb_city.csv')
        
        # Define border keywords for categorization
        self.border_keywords = {
            'Street': ['شارع', 'طريق','Street','street','شوارع','شلرع','نافذ','شار ع'],
            'Building': ['مبنى', 'منزل', 'محل', 'بناء','بيت', 'جار', 'مزرعة','Neighbor','overnmental','acility','مسجد'],
            'Empty_Plot': ['قطعه','فضاء','ساحة', 'خالي','ارض' ,'أرض', 'قطعة','part','Part','مخطط','الارض','رقم','الــقـــطــعــة','الـقـطـعـة','فناء','فسحة','قطة','القطع','برحة'],
            'Alley':['ممر','مشاة','lley'],
            'Parking':['سيارات','arking','مواقف'],
            'Public_space':['حديقة','ميدان','حديقه']
        }
        
        self.border_columns = ['NorthBorder', 'SouthBorder', 'East_order', 'WestBorder']
        
        # Define mapping from border type to length columns
        self.border_to_length_map = {
            'NorthBorder_Type': 'LengthFromNorth',
            'SouthBorder_Type': 'LengthFromSouth',
            'East_order_Type': 'LengthFromEast',
            'WestBorder_Type': 'LengthFromWest'
        }

        # Define the exact columns that the model was trained on
        self.training_columns = [
            'Area', 'LengthFromNorth', 'LengthFromSouth', 'LengthFromEast',
            'LengthFromWest', 'StreetWidth', 'distance_from_center_km', 'Perimeter',
            'Street_Frontage', 'Num_Street_Fronts', 'Encoded_Hood', 'Encoded_City',
            'Latitude', 'Longitude',
            'PropAssetRegionName_Asir', 'PropAssetRegionName_Bahah',
            'PropAssetRegionName_Eastern Province', 'PropAssetRegionName_Hail',
            'PropAssetRegionName_Jawf', 'PropAssetRegionName_Jizan',
            'PropAssetRegionName_Madinah', 'PropAssetRegionName_Makkah',
            'PropAssetRegionName_Najran', 'PropAssetRegionName_Northern Borders',
            'PropAssetRegionName_Qassim', 'PropAssetRegionName_Riyadh',
            'PropAssetRegionName_Tabuk', 'EvaluationAssetTypeName_Commercial Land',
            'EvaluationAssetTypeName_Farming Land', 'EvaluationAssetTypeName_Housing Land',
            'EvaluationAssetTypeName_Raw Land', 'NorthBorder_Type_Alley',
            'NorthBorder_Type_Building', 'NorthBorder_Type_Empty_Plot',
            'NorthBorder_Type_Other', 'NorthBorder_Type_Parking',
            'NorthBorder_Type_Public_space', 'NorthBorder_Type_Street',
            'SouthBorder_Type_Alley', 'SouthBorder_Type_Building',
            'SouthBorder_Type_Empty_Plot', 'SouthBorder_Type_Other',
            'SouthBorder_Type_Parking', 'SouthBorder_Type_Public_space',
            'SouthBorder_Type_Street', 'East_order_Type_Alley',
            'East_order_Type_Building', 'East_order_Type_Empty_Plot',
            'East_order_Type_Other', 'East_order_Type_Parking',
            'East_order_Type_Public_space', 'East_order_Type_Street',
            'WestBorder_Type_Alley', 'WestBorder_Type_Building',
            'WestBorder_Type_Empty_Plot', 'WestBorder_Type_Other',
            'WestBorder_Type_Parking', 'WestBorder_Type_Public_space',
            'WestBorder_Type_Street', 'AssetLevelId_A', 'AssetLevelId_B',
            'AssetLevelId_C', 'AssetLevelId_D'
        ]
    
    def get_border_type(self, border_description: str) -> str:
        """
        Categorizes a border based on keywords in its description.
        Returns 'Other' if no specific keyword is found.
        
        Args:
            border_description (str): Description of the border
            
        Returns:
            str: Category of the border
        """
        if pd.isna(border_description):
            return 'Other'
        
        border_description_lower = str(border_description).lower()
        for type_name, keywords in self.border_keywords.items():
            if any(keyword in border_description_lower for keyword in keywords):
                return type_name
        return 'Other'  # Default if no keywords match
    
    def haversine(self, lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """
        Calculate the great circle distance in kilometers between two points
        on the earth (specified in decimal degrees)
        
        Args:
            lat1 (float): Latitude of first point
            lon1 (float): Longitude of first point
            lat2 (float): Latitude of second point
            lon2 (float): Longitude of second point
            
        Returns:
            float: Distance in kilometers
        """
        # Convert decimal degrees to radians
        lon1, lat1, lon2, lat2 = map(np.radians, [lon1, lat1, lon2, lat2])

        # Haversine formula
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = np.sin(dlat/2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2)**2
        c = 2 * np.arcsin(np.sqrt(a))
        r = 6371  # Radius of earth in kilometers
        return c * r
    
    def preprocess_features(self, features: Dict[str, Any]) -> np.ndarray:
        """
        Preprocess the input features.
        
        Args:
            features (Dict[str, Any]): Dictionary containing feature values
            
        Returns:
            np.ndarray: Preprocessed features ready for model prediction
        """
        print("\n=== Starting Preprocessing ===")
        print("Input features:", features)
        
        # Convert input dictionary to DataFrame
        df = pd.DataFrame([features])
        print("\n=== After DataFrame Conversion ===")
        print(df)
        
        # Apply feature engineering
        df = self._apply_feature_engineering(df)
        print("\n=== After Feature Engineering ===")
        print(df)
        
        # Preprocess categorical features
        df = self._preprocess_categorical_features(df)
        print("\n=== After Categorical Preprocessing ===")
        print(df)
        
        # Preprocess numeric features
        df = self._preprocess_numeric_features(df)
        print("\n=== After Numeric Preprocessing ===")
        print(df)
        
        # Combine all features
        processed_features = self._combine_features(df)
        print("\n=== Final Processed Features ===")
        print(processed_features)
        
        return processed_features
    
    def _apply_feature_engineering(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Apply feature engineering steps.
        
        Args:
            df (pd.DataFrame): Input DataFrame
            
        Returns:
            pd.DataFrame: DataFrame with engineered features
        """
        print("\n=== Starting Feature Engineering ===")
        
        # Get city center coordinates for the input city
        city_center = self.city_centers[
            self.city_centers['City_en'] == df['PropAssetCityName'].iloc[0]
        ]
        print("City center data:", city_center)
        
        if not city_center.empty:
            # Calculate distance from city center
            df['distance_from_center_km'] = self.haversine(
                df['Latitude'].iloc[0],
                df['Longitude'].iloc[0],
                city_center['City_Center_Lat'].iloc[0],
                city_center['City_Center_Lon'].iloc[0]
            )
            print("Distance from center calculated:", df['distance_from_center_km'].iloc[0])
        else:
            # If city not found, set distance to None
            df['distance_from_center_km'] = None
            print("City not found in city_centers, distance set to None")
        
        # Add border type features
        for col in self.border_columns:
            if col in df.columns:
                df[f'{col}_Type'] = df[col].apply(self.get_border_type)
                print(f"Border type for {col}:", df[f'{col}_Type'].iloc[0])
        
        # Calculate perimeter
        df['Perimeter'] = (
            df['LengthFromNorth'] + 
            df['LengthFromSouth'] + 
            df['LengthFromEast'] + 
            df['LengthFromWest']
        )
        print("Perimeter calculated:", df['Perimeter'].iloc[0])
        
        # Initialize street frontage features
        df['Street_Frontage'] = 0.0
        df['Num_Street_Fronts'] = 0
        
        # Calculate street frontage and number of street fronts
        for border_type_col, length_col in self.border_to_length_map.items():
            if border_type_col in df.columns and length_col in df.columns:
                # Add to Street_Frontage if the border type is 'Street'
                df['Street_Frontage'] += np.where(
                    df[border_type_col] == 'Street',
                    df[length_col],
                    0
                )
                # Increment Num_Street_Fronts if the border type is 'Street'
                df['Num_Street_Fronts'] += np.where(
                    df[border_type_col] == 'Street',
                    1,
                    0
                )
        print("Street frontage calculated:", df['Street_Frontage'].iloc[0])
        print("Number of street fronts:", df['Num_Street_Fronts'].iloc[0])
        
        # Add Encoded_Hood and Encoded_City features
        hood = df['PropAssetNeighborhoodName'].iloc[0]
        city = df['PropAssetCityName'].iloc[0]
        
        # First try to find exact match for both neighborhood and city
        match = self.encoded_neighb_city[
            (self.encoded_neighb_city['PropAssetNeighborhoodName'] == hood) &
            (self.encoded_neighb_city['PropAssetCityName'] == city)
        ]
        
        if not match.empty:
            # Found exact match for both neighborhood and city
            df['Encoded_Hood'] = match['Encoded_Hood'].iloc[0]
            df['Encoded_City'] = match['Encoded_City'].iloc[0]
        else:
            # If no exact match, try to find city match and use its encoding
            city_match = self.encoded_neighb_city[
                self.encoded_neighb_city['PropAssetCityName'] == city
            ]
            if not city_match.empty:
                # Use the city's encoding for both hood and city
                df['Encoded_Hood'] = city_match['Encoded_City'].iloc[0]
                df['Encoded_City'] = city_match['Encoded_City'].iloc[0]
                print(f"Using city encoding as fallback for neighborhood: {hood} in city: {city}")
            else:
                # If no city match either, set both to NaN
                df['Encoded_Hood'] = np.nan
                df['Encoded_City'] = np.nan
                print(f"No encoding found for neighborhood: {hood} or city: {city}")
        
        return df
    
    def _preprocess_categorical_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Preprocess categorical features using one-hot encoding.
        
        Args:
            df (pd.DataFrame): Input DataFrame
            
        Returns:
            pd.DataFrame: DataFrame with preprocessed categorical features
        """
        print("\n=== Starting Categorical Preprocessing ===")
        
        # Process original categorical columns
        for col in self.categorical_columns:
            if col in df.columns:
                print(f"\nProcessing categorical column: {col}")
                if col not in self.encoders:
                    print(f"Creating new encoder for {col}")
                    self.encoders[col] = OneHotEncoder(sparse_output=False, handle_unknown='ignore')
                    self.encoders[col].fit(df[[col]])
                
                # Transform the feature
                encoded = self.encoders[col].transform(df[[col]])
                encoded_df = pd.DataFrame(
                    encoded,
                    columns=[f"{col}_{cat}" for cat in self.encoders[col].categories_[0]],
                    index=df.index
                )
                print(f"Encoded columns for {col}:", encoded_df.columns.tolist())
                
                # Drop original column and add encoded columns
                df = df.drop(col, axis=1)
                df = pd.concat([df, encoded_df], axis=1)
        
        return df
    
    def _preprocess_numeric_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Preprocess numeric features.
        This method will be extended with specific numeric preprocessing steps.
        
        Args:
            df (pd.DataFrame): Input DataFrame
            
        Returns:
            pd.DataFrame: DataFrame with preprocessed numeric features
        """
        print("\n=== Starting Numeric Preprocessing ===")
        
        # Apply log transformation to specified numeric columns
        numeric_columns = [
            'Area', 'LengthFromNorth', 'LengthFromSouth', 'LengthFromEast',
            'LengthFromWest', 'StreetWidth', 'Latitude', 'Longitude',
            'distance_from_center_km', 'SARm2', 'Perimeter', 'Street_Frontage',
            'Num_Street_Fronts', 'Encoded_Hood', 'Encoded_City',
        ]
        columns_to_log = ['Area', 'LengthFromNorth', 'LengthFromSouth', 'LengthFromEast',
            'LengthFromWest', 'Perimeter', 'distance_from_center_km']
        
        columns_to_sqrt = ['Encoded_Hood', 'StreetWidth']

        # Apply log transformation
        for col in columns_to_log:
            if col in df.columns:
                print(f"\nProcessing numeric column with log transform: {col}")
                print(f"Original value: {df[col].iloc[0]}")
                # Fill None/NaN values with 0 before log transformation
                df[col] = df[col].fillna(0)
                # Apply log1p transformation
                df[col] = np.log1p(df[col])
                print(f"Transformed value: {df[col].iloc[0]}")
        
        # Apply sqrt transformation
        for col in columns_to_sqrt:
            if col in df.columns:
                print(f"\nProcessing numeric column with sqrt transform: {col}")
                print(f"Original value: {df[col].iloc[0]}")
                # Fill None/NaN values with 0 before sqrt transformation
                df[col] = df[col].fillna(0)
                # Apply sqrt transformation
                df[col] = np.sqrt(df[col])
                print(f"Transformed value: {df[col].iloc[0]}")
        
        # Ensure all required columns exist
        for col in numeric_columns:
            if col not in df.columns:
                df[col] = 0
        
        # Apply standard scaling to all numeric columns using pre-trained scaler
        print(f"\nScaling numeric column")
        numeric_data = df[numeric_columns].fillna(0)
        scaled_data = self.scaler.transform(numeric_data)
        df[numeric_columns] = scaled_data
        
        # Set pandas display options to show all columns and rows
        pd.set_option('display.max_columns', None)
        pd.set_option('display.width', None)
        pd.set_option('display.max_rows', None)
        print("\nScaled data:")
        print(df[numeric_columns].to_string())
        
        return df
    
    def _combine_features(self, df: pd.DataFrame) -> np.ndarray:
        """
        Combine all features into a single numpy array, ensuring the same structure as training data.
        
        Args:
            df (pd.DataFrame): Input DataFrame with all preprocessed features
            
        Returns:
            np.ndarray: Combined features ready for model prediction
        """
        print("\n=== Starting Feature Combination ===")
        print("Current columns:", df.columns.tolist())
        
        # Reindex the DataFrame to match training columns
        df = df.reindex(columns=self.training_columns, fill_value=0)
        
        print("Final columns after reindexing:", df.columns.tolist())
        print("Final feature shape:", df.shape)
        
        # Return DataFrame instead of numpy array to preserve feature names
        return df 