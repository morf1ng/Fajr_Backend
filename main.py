from fastapi import FastAPI, HTTPException
import httpx

app = FastAPI()

ALADHAN_API_URL = "http://api.aladhan.com/v1/timings"

@app.get("/")
def read_root():
    return {"message": "Welcome to the Prayer Times API!"}

@app.get("/prayer-times/{latitude}/{longitude}")
async def get_prayer_times(latitude: float, longitude: float):
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "method": 2 
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.get(ALADHAN_API_URL, params=params)
        
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Error fetching prayer times")
        
        data = response.json()
        return data["data"]["timings"]
