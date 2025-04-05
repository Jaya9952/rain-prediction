from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import joblib
import numpy as np
from datetime import datetime


model = joblib.load("rain_model.pkl")
scaler = joblib.load("scaler.pkl")
label_encoder = joblib.load("label_encoder.pkl")

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class WeatherInput(BaseModel):
    location: str
    date: str  

def preprocess_input(data: WeatherInput):
    try:
        location_encoded = label_encoder.transform([data.location])[0]
    except ValueError:
        return {"error": "Invalid location. Please enter a valid state/UT name."}

    try:
        month = datetime.strptime(data.date, "%Y-%m-%d").month
    except ValueError:
        return {"error": "Invalid date format. Use YYYY-MM-DD."}

   
    input_data = np.array([[location_encoded, month]])
    input_scaled = scaler.transform(input_data)
    return input_scaled

@app.post("/predict")
async def predict_rain(data: WeatherInput):
    processed_input = preprocess_input(data)

    if isinstance(processed_input, dict): 
        return processed_input

    prediction = model.predict(processed_input)[0]
    rain_prediction = "High" if prediction == 1 else "Low"

    return {
        "rain_prediction": rain_prediction,
        "date": data.date
    }


