from fastapi import FastAPI, APIRouter, Depends, HTTPException
import requests
from sqlalchemy.orm import Session
from app.database import SessionLocal, WeatherData
from app.ml.predict import predict_rainfall
import csv
import os
from dotenv import load_dotenv
from app.auth import get_current_user
from datetime import datetime

# Load environment variables
load_dotenv()

OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
BASE_URL = os.getenv("BASE_URL")
FORECAST_URL = os.getenv("FORECAST_URL")

router = APIRouter()

# File path for storing weather data
CSV_FILE = "data_source/weather_data.csv"

# Ensure directory exists
os.makedirs(os.path.dirname(CSV_FILE), exist_ok=True)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/current_weather")
def get_current_weather(city: str, db: Session = Depends(get_db), user: dict = Depends(get_current_user)):
    print(f"Received request for current weather of city: {city}")
    
    url = f"{BASE_URL}?q={city}&appid={OPENWEATHER_API_KEY}&units=metric"
    response = requests.get(url)

    if response.status_code != 200:
        raise HTTPException(status_code=404, detail="City not found")

    data = response.json()

    # Extract relevant weather features safely
    temperature = data.get("main", {}).get("temp", None)
    humidity = data.get("main", {}).get("humidity", None)
    pressure = data.get("main", {}).get("pressure", None)
    wind_speed = data.get("wind", {}).get("speed", None)
    rainfall = data.get("rain", {}).get("1h", 0)

    # Store in database
    weather_entry = WeatherData(
        city=city,
        temperature=temperature,
        humidity=humidity,
        pressure=pressure,
        wind_speed=wind_speed,
        rainfall=rainfall
    )
    db.add(weather_entry)
    db.commit()
    db.refresh(weather_entry)

    # Store in CSV
    save_weather_data_to_csv(city, temperature, humidity, pressure, wind_speed, rainfall, weather_entry.timestamp)

    return {
        "city": city,
        "temperature": temperature,
        "humidity": humidity,
        "pressure": pressure,
        "wind_speed": wind_speed,
        "rainfall": rainfall,
        "timestamp": weather_entry.timestamp
    }

def save_weather_data_to_csv(city, temperature, humidity, pressure, wind_speed, rainfall, timestamp):
    """Save weather data to CSV file"""
    file_exists = os.path.isfile(CSV_FILE)

    with open(CSV_FILE, mode="a", newline="") as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["city", "temperature", "humidity", "pressure", "wind_speed", "rainfall", "timestamp"])  # Header
        writer.writerow([city, temperature, humidity, pressure, wind_speed, rainfall, timestamp])

@router.get("/forecast")
def get_weather_forecast(city: str, db: Session = Depends(get_db)):
    print(f"Received request for forecast of city: {city}")

    url = f"{FORECAST_URL}?q={city}&appid={OPENWEATHER_API_KEY}&units=metric"
    response = requests.get(url)

    if response.status_code != 200:
        raise HTTPException(status_code=404, detail="City not found")

    data = response.json()
    forecast_data = []

    for item in data["list"]:
        temp = item["main"]["temp"]
        humidity = item["main"]["humidity"]
        pressure = item["main"]["pressure"]
        wind_speed = item["wind"]["speed"]

        # Predict rainfall using ML model
        will_rain = predict_rainfall(temp, humidity, pressure, wind_speed)

        forecast_data.append({
            "datetime": item["dt_txt"],
            "temperature": temp,
            "humidity": humidity,
            "pressure": pressure,
            "wind_speed": wind_speed,
            "rainfall_prediction": "Yes" if will_rain else "No"
        })

    return {"city": city, "forecast": forecast_data}
