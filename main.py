from fastapi import FastAPI, HTTPException
from prayer_times import get_prayer_times
from hadith_api import hadith_of_the_day
import uvicorn
from typing import Optional
from quran_api import get_ayah, get_surah, get_surah_ar
from azan_player.player import AzanPlayer


app = FastAPI()
azan_player = AzanPlayer()

@app.get("/")
def read_root():
    return {"message": "Добро пожаловать в Islamic API!"}

@app.get("/prayer-times/{latitude}/{longitude}")
async def prayer_times_endpoint(latitude: float, longitude: float):
    return await get_prayer_times(latitude, longitude)

@app.get("/hadith-of-the-day")
async def hadith_of_the_day_endpoint():
    return await hadith_of_the_day()


@app.get("/quran/surah/{surah_number}")
async def get_surah_endpoint(surah_number: int, edition: Optional[str] = "ru.kuliev"):
    return await get_surah(surah_number, edition)

@app.get("/quran/ayah/{surah_number}/{ayah_number}")
async def get_ayah_endpoint(surah_number: int, ayah_number: int, edition: Optional[str] = "ru.kuliev"):
    return await get_ayah(surah_number, ayah_number, edition)

@app.get("/quran/surah_ar/{surah_number}")
async def get_surah_ar_endpoint(surah_number: int, edition: Optional[str] = None):
    return await get_surah_ar(surah_number, edition)



@app.get("/play-azan")
async def play_azan(azan_number: int, volume: float = 1.0):
    try:
        azan_player.play_azan(azan_number, volume)
        return {
            "status": "playing",
            "azan_number": azan_number,
            "volume": volume
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/stop-azan")
async def stop_azan():
    azan_player.stop()
    return {"status": "stopped"}

@app.get("/azan-status")
async def get_status():
    return azan_player.get_status()



