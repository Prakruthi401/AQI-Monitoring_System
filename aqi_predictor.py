import pandas as pd
import numpy as np
import joblib
import json
import os
from datetime import datetime, timedelta

class AQIPredictor:
    """Use trained ensemble models for AQI prediction"""
    
    def __init__(self):
        self.models_dir = 'models'
        self.data_dir = 'data'
        self.models_loaded = False
        self.load_models()
    
    def load_models(self):
        """Load trained models"""
        try:
            # Load feature columns
            with open(f'{self.data_dir}/feature_columns.json', 'r') as f:
                self.feature_cols = json.load(f)
            
            # Load sklearn scaler
            self.sklearn_scaler = joblib.load(f'{self.models_dir}/sklearn_scaler.pkl')
            
            # Load sklearn models
            self.random_forest = joblib.load(f'{self.models_dir}/random_forest.pkl')
            self.gradient_boosting = joblib.load(f'{self.models_dir}/gradient_boosting.pkl')
            self.adaboost = joblib.load(f'{self.models_dir}/adaboost.pkl')
            self.ridge = joblib.load(f'{self.models_dir}/ridge.pkl')
            self.elastic_net = joblib.load(f'{self.models_dir}/elastic_net.pkl')
            self.svr = joblib.load(f'{self.models_dir}/svr.pkl')
            
            # Load LSTM model
            from tensorflow.keras.models import load_model
            self.lstm_model = load_model(f'{self.models_dir}/lstm_advanced_best.h5')
            self.lstm_scaler = joblib.load(f'{self.models_dir}/lstm_scaler.pkl')
            
            # Load training metrics
            with open(f'{self.models_dir}/training_metrics.json', 'r') as f:
                self.metrics = json.load(f)
            
            self.models_loaded = True
            print(f"Models loaded successfully. Ensemble accuracy: {self.metrics['Accuracy']:.2f}%")
            
        except Exception as e:
            print(f"Error loading models: {e}")
            self.models_loaded = False
    
    def prepare_features(self, data):
        """Prepare features for prediction"""
        df = pd.DataFrame([data])
        
        # Ensure all feature columns exist
        for col in self.feature_cols:
            if col not in df.columns:
                df[col] = 0
        
        # Fill missing values
        df = df[self.feature_cols].fillna(0)
        
        return df
    
    def predict_ensemble(self, current_data):
        """Make prediction using ensemble of sklearn models"""
        if not self.models_loaded:
            return None, None
        
        try:
            # Prepare features
            features = self.prepare_features(current_data)
            features_scaled = self.sklearn_scaler.transform(features)
            
            # Get predictions from each model
            predictions = {
                'random_forest': self.random_forest.predict(features_scaled)[0],
                'gradient_boosting': self.gradient_boosting.predict(features_scaled)[0],
                'adaboost': self.adaboost.predict(features_scaled)[0],
                'ridge': self.ridge.predict(features_scaled)[0],
                'elastic_net': self.elastic_net.predict(features_scaled)[0],
                'svr': self.svr.predict(features_scaled)[0]
            }
            
            # Weighted ensemble
            weights = {
                'random_forest': 0.25,
                'gradient_boosting': 0.25,
                'adaboost': 0.15,
                'ridge': 0.1,
                'elastic_net': 0.1,
                'svr': 0.15
            }
            
            ensemble_pred = sum(weights[name] * pred for name, pred in predictions.items())
            
            return ensemble_pred, predictions
            
        except Exception as e:
            print(f"Error in ensemble prediction: {e}")
            return None, None
    
    def predict_lstm(self, historical_data, sequence_length=24):
        """Make prediction using LSTM model"""
        if not self.models_loaded:
            return None
        
        try:
            # Prepare sequence
            df = pd.DataFrame(historical_data)
            
            # Ensure all feature columns exist
            for col in self.feature_cols:
                if col not in df.columns:
                    df[col] = 0
            
            # Get last sequence_length rows
            if len(df) < sequence_length:
                # Pad with zeros if not enough data
                padding = pd.DataFrame(0, index=range(sequence_length - len(df)), columns=df.columns)
                df = pd.concat([padding, df], ignore_index=True)
            
            sequence = df.tail(sequence_length)[self.feature_cols].values.astype(np.float32)
            
            # Scale
            sequence_scaled = self.lstm_scaler.transform(sequence.reshape(-1, sequence.shape[-1]))
            sequence_scaled = sequence_scaled.reshape(1, sequence_length, -1)
            
            # Predict
            prediction = self.lstm_model.predict(sequence_scaled)[0][0]
            
            return prediction
            
        except Exception as e:
            print(f"Error in LSTM prediction: {e}")
            return None
    
    def predict_future_hours(self, current_data, current_aqi, hours_ahead=[1, 6, 12, 24]):
        """Predict AQI for future hours using current AQI as base"""
        if not self.models_loaded:
            return None
        
        predictions = {}
        
        # Use current AQI as base (persistence baseline)
        base_aqi = current_aqi
        
        # Get ensemble prediction for trend direction
        ensemble_pred, individual_preds = self.predict_ensemble(current_data)
        
        # Calculate trend direction from ensemble prediction vs current
        if ensemble_pred is not None:
            trend_ratio = ensemble_pred / (base_aqi + 1)  # Avoid division by zero
            # Clamp trend ratio to realistic range (0.8 to 1.2)
            trend_ratio = max(0.8, min(1.2, trend_ratio))
        else:
            trend_ratio = 1.0  # No change if ensemble fails
        
        # Apply time-based adjustments with realistic bounds
        current_hour = datetime.now().hour
        
        for hour in hours_ahead:
            future_hour = (current_hour + hour) % 24
            
            # Diurnal pattern adjustment (smaller changes)
            if 6 <= future_hour <= 18:  # Daytime - typically higher
                time_adjustment = 1.0 + 0.05 * np.sin(np.pi * (future_hour - 6) / 12)
            else:  # Nighttime - typically lower
                time_adjustment = 0.95 + 0.03 * np.sin(np.pi * (future_hour - 18) / 12)
            
            # Combine trend and time adjustments (gradual change)
            # Trend influence decreases with time horizon
            trend_influence = max(0.3, 1.0 - (hour / 48))  # Decreases over time
            combined_adjustment = (trend_ratio * trend_influence) + (time_adjustment * (1 - trend_influence))
            
            # Calculate predicted AQI
            predicted_aqi = base_aqi * combined_adjustment
            
            # Add realistic bounds based on current AQI
            # AQI can't drop more than 30% in 1 hour or rise more than 40%
            max_change_1h = 0.4
            max_change_6h = 0.6
            max_change_12h = 0.8
            max_change_24h = 1.0
            
            if hour == 1:
                max_change = max_change_1h
            elif hour == 6:
                max_change = max_change_6h
            elif hour == 12:
                max_change = max_change_12h
            else:
                max_change = max_change_24h
            
            # Apply bounds
            min_aqi = base_aqi * (1 - max_change)
            max_aqi = base_aqi * (1 + max_change)
            predicted_aqi = max(min_aqi, min(max_aqi, predicted_aqi))
            
            # Ensure minimum AQI of 10 (realistic minimum)
            predicted_aqi = max(10, predicted_aqi)
            
            predictions[hour] = predicted_aqi
        
        return predictions
    
    def get_model_info(self):
        """Get information about trained models"""
        if not self.models_loaded:
            return None
        
        return {
            'ensemble_accuracy': self.metrics['Accuracy'],
            'mae': self.metrics['MAE'],
            'rmse': self.metrics['RMSE'],
            'mape': self.metrics['MAPE'],
            'r2': self.metrics['R²'],
            'models': ['Random Forest', 'Gradient Boosting', 'AdaBoost', 'Ridge', 'Elastic Net', 'SVR', 'LSTM']
        }

# Global predictor instance
predictor = AQIPredictor()
