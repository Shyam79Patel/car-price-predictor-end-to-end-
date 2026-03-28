from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, field_validator
import joblib 
import numpy as np
import pandas as pd
from database import init_db, save_prediction, get_predictions

app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"], 
    )

init_db()

try:
    model = joblib.load('car_model.joblib')
except Exception as e:
    raise RuntimeError(f'Model failed to load: {e}')

class CarFeature(BaseModel):
    brand : str = Field(..., example='Mahindra', description='Brand Name Of the Car')
    car_model : str = Field(..., example='Scorpio N', description='Model Name of the Car')
    vehicle_age : int = Field(..., ge=0, le=30, example=5, description='Age of the Car')
    km_driven : int = Field(..., ge=0, le=1000000, example=25000, description='Total KMs Driven')
    seller_type : str = Field(..., example='Dealer')
    fuel_type : str = Field(..., example='Petrol')
    transmission_type : str = Field(..., example='Manual')
    mileage: float = Field(..., ge=0, le=50, example=18.5, description='Mileage in km per litre')
    engine: float = Field(..., ge=500, le=6000, example=2200, description='Engine capacity in CC')
    max_power: float = Field(..., ge=30, le=600, example=200, description='Max power in BHP')
    seats: int = Field(..., ge=2, le=10, example=5, description='Number of seats')

    @field_validator('seller_type')
    @classmethod
    def validate_seller_type(cls, v):
        allowed = ['Dealer', 'Individual', 'Trustmark Dealer']
        if v not in allowed:
            raise ValueError(f'seller_type msut be one of {allowed}')
        return v

    @field_validator('fuel_type')
    @classmethod
    def validate_fuel_type(cls, v):
        allowed = ['Petrol', 'Diesel', 'CNG', 'LPG', 'Electric']
        if v not in allowed:
            raise ValueError(f'fuel_type must be one of {allowed}')
        return v

    @field_validator('transmission_type')
    @classmethod
    def validate_transmission(cls, v):
        allowed = ['Manual', 'Automatic']
        if v not in allowed:
            raise ValueError(f'transmission_type must be one of {allowed}')
        return v

    @field_validator('brand', 'car_model')
    @classmethod
    def must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError('Field cannot be empty')
        return v.strip().title()
    
class PredictionResponse(BaseModel):
    predicted_price : str
    predicted_price_raw : float
    input_summary : dict

@app.get('/', tags=['Health'])
def home():
    return {
        'status': 'running',
        'message': 'Used Car Price Prediction API',
        'version': '1.0.0',
        'docs': '/docs'
    }

@app.get('/health', tags=['Health'])
def health_check():
    return {'status': 'healthy', 'model_loaded': model is not None}

@app.post('/predict', response_model = PredictionResponse, tags=['Predition'])
def predict(car : CarFeature):
    try:
        input_df = pd.DataFrame([car.model_dump()])

        input_df['brand_encoded'] = 1
        input_df['model_encoded'] = 1
        input_df.drop(columns=['brand', 'car_model'], inplace=True)
        
        log_price = model.predict(input_df)
        actual_price = np.exp(log_price[0])

        save_prediction(
        brand = car.brand,
        car_model = car.car_model,
        vehicle_age = car.vehicle_age,
        km_driven = car.km_driven,
        fuel_type = car.fuel_type,
        transmission_type = car.transmission_type,
        predicted_price = round(float(actual_price), 2))
        
        return PredictionResponse(predicted_price=f'₹{int(actual_price):,}',
                                  predicted_price_raw=round(float(actual_price), 2),
                                  input_summary={
                                      'brand' : car.brand,
                                      'car_model' : car.car_model,
                                      'vehicle_age' : car.vehicle_age,
                                      'fuel_type' : car.fuel_type,
                                      'transmission_type' : car.transmission_type
                                  })
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Prediction failed : {str(e)}')
    
@app.get('/history', tags=['History'])
def history():
    rows = get_predictions()
    return {
        'total_predictions': len(rows),
        'predictions': [
            {
                'id': r[0],
                'brand': r[1],
                'car_model': r[2],
                'vehicle_age': r[3],
                'km_driven': r[4],
                'fuel_type': r[5],
                'transmission_type': r[6],
                'predicted_price': f'₹{int(r[7]):,}',
                'timestamp': r[8]
            }
            for r in rows
        ]
    }