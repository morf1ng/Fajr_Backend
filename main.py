from fastapi import FastAPI
from prayer_times import get_prayer_times
from hadith_api import hadith_of_the_day
import uvicorn

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Добро пожаловать в Islamic API!"}

@app.get("/prayer-times/{latitude}/{longitude}")
async def prayer_times_endpoint(latitude: float, longitude: float):
    return await get_prayer_times(latitude, longitude)

@app.get("/hadith-of-the-day")
async def hadith_of_the_day_endpoint():
    return await hadith_of_the_day()

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)