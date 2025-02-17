from app.routes.weather import router as weather_router
from app.auth import router as auth_router
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from fastapi import FastAPI

app = FastAPI()

#Add CORS middlwware
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # Adjust this to specify allowed origins
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
app.include_router(weather_router, prefix="/weather", tags=["Weather"])


if __name__=="__main__":
    uvicorn.run(app, host="127.0.0.1", port=8080)
