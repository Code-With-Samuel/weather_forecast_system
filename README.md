# Weather Forecasting System

This project is a FastAPI-based weather forecasting system that uses real-time OpenWeather API data and machine learning for rainfall prediction.

## Features
- User authentication (JWT)
- Fetch current weather data
- Predict rainfall using ML
- Store data in SQLite & CSV

## Installation
```sh
git clone https://github.com/your-repo.git
cd weather_forecast_backend
pip install -r requirements.txt
uvicorn main:app --reload
