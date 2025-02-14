from fastapi import FastAPI
from app.routes.weather import router as weather_router
from app.auth import router as auth_router
import uvicorn

app = FastAPI()

app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
app.include_router(weather_router, prefix="/weather", tags=["Weather"])


if __name__=="__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
