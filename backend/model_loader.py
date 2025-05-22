import pickle
import numpy as np
from typing import Dict, Any
from sklearn.ensemble import GradientBoostingRegressor
from preprocessing import FeaturePreprocessor

class ModelLoader:
    def __init__(self, model_path: str, target_scaler_path: str = None, standard_scaler_path: str = None):
        """
        Initialize the model loader.
        
        Args:
            model_path (str): Path to the pickled GradientBoostingRegressor model file
            target_scaler_path (str, optional): Path to the target scaler file. If None, will look for target_scaler.pkl in the same directory.
            standard_scaler_path (str, optional): Path to the standard scaler file. If None, will look for standard_scaler.pkl in the same directory.
        """
        try:
            # Load the model
            with open(model_path, 'rb') as f:
                self.model = pickle.load(f)
            
            # Verify model type and reinitialize if needed
            if not isinstance(self.model, GradientBoostingRegressor):
                raise ValueError("Loaded model is not a GradientBoostingRegressor")
            
            # Initialize preprocessor
            self.preprocessor = FeaturePreprocessor()
            
            # Load the target scaler
            target_scaler_path = target_scaler_path or 'target_scaler.pkl'
            try:
                with open(target_scaler_path, 'rb') as f:
                    self.target_scaler = pickle.load(f)
            except FileNotFoundError:
                print(f"Warning: {target_scaler_path} not found. Predictions will not be inverse scaled.")
                self.target_scaler = None

            # Load the standard scaler
            standard_scaler_path = standard_scaler_path or 'standard_scaler.pkl'
            try:
                with open(standard_scaler_path, 'rb') as f:
                    self.standard_scaler = pickle.load(f)
            except FileNotFoundError:
                print(f"Warning: {standard_scaler_path} not found. Feature scaling may be affected.")
                self.standard_scaler = None
                
        except Exception as e:
            raise Exception(f"Error loading model: {str(e)}")
    
    def predict(self, features: Dict[str, Any]) -> tuple:
        """
        Make predictions using the loaded model.
        
        Args:
            features (Dict[str, Any]): Dictionary containing feature values
            
        Returns:
            tuple: (prediction, None) - GradientBoostingRegressor doesn't provide probabilities
        """
        try:
            # Preprocess features
            processed_features = self.preprocessor.preprocess_features(features)
            
            # Ensure features are in the correct order
            if hasattr(processed_features, 'columns'):
                processed_features = processed_features[self.preprocessor.training_columns]
            
            # Make prediction using DataFrame with feature names
            prediction = self.model.predict(processed_features)[0]
            
            # Inverse transform the standard scaling if scaler exists
            if self.target_scaler is not None:
                prediction = self.target_scaler.inverse_transform([[prediction]])[0][0]
            
            # Apply inverse log transformation (expm1) to get back to original scale
            prediction = np.expm1(prediction)
            
            # Convert prediction to float to ensure JSON serialization
            prediction = float(prediction)
            
            print(f"Raw prediction: {prediction}")
            return prediction, None
            
        except Exception as e:
            print(f"Error in prediction: {str(e)}")
            print(f"Processed features shape: {processed_features.shape}")
            print(f"Processed features columns: {processed_features.columns if hasattr(processed_features, 'columns') else 'No columns'}")
            raise Exception(f"Error making prediction: {str(e)}") 