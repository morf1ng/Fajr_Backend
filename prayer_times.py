from fastapi import FastAPI, HTTPException
import httpx
from datetime import datetime, timedelta
import uvicorn
app = FastAPI()

ALADHAN_API_URL = "http://api.aladhan.com/v1/timings"

@app.get("/")
def read_root():
    return {"message": "Добро пожаловать в API времени молитв!"}

@app.get("/prayer-times/{latitude}/{longitude}")
async def get_prayer_times(latitude: float, longitude: float):
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "method": 3
    }
    
    current_date = datetime.now().strftime("%d-%m-%Y")
    
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{ALADHAN_API_URL}/{current_date}", params=params)
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Ошибка при получении времени молитв")
        
        data = response.json()
        
        timings = data["data"]["timings"]
        filtered_timings = {
            "Fajr": timings["Fajr"],
            "Sunrise": timings["Sunrise"],
            "Dhuhr": timings["Dhuhr"],
            "Asr": timings["Asr"],
            "Sunset": timings["Sunset"],
            "Maghrib": timings["Maghrib"],
            "Isha": timings["Isha"]
        }
        
     
        tune_offsets = [1,-2,5,2,4,4,-12] 
        prayer_names = ["Fajr", "Sunrise", "Dhuhr", "Asr", "Sunset", "Maghrib", "Isha"]
        
        for i, offset in enumerate(tune_offsets):
            if i < len(prayer_names):
                prayer_name = prayer_names[i]
                if prayer_name in filtered_timings:
                    prayer_time = datetime.strptime(filtered_timings[prayer_name], "%H:%M")
                    adjusted_time = prayer_time + timedelta(minutes=offset)
                    filtered_timings[prayer_name] = adjusted_time.strftime("%H:%M")
        
        return filtered_timings