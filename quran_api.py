from fastapi import HTTPException
import httpx
from typing import Optional

QURAN_API_URL = "https://api.alquran.cloud/v1"

async def get_surah(surah_number: int, edition: Optional[str] = "ru.kuliev"):

    if not 1 <= surah_number <= 114:
        raise HTTPException(status_code=400, detail="Номер суры должен быть от 1 до 114")
    
    try:
        async with httpx.AsyncClient() as client:
           
            response = await client.get(
                f"{QURAN_API_URL}/surah/{surah_number}/{edition}"
            )
            response.raise_for_status()
            return response.json()
    except httpx.HTTPStatusError as e:
        raise HTTPException(
            status_code=e.response.status_code,
            detail=f"Ошибка при получении суры: {str(e)}"
        )

async def get_surah_ar(surah_number: int, edition: Optional[str] = None):

    if not 1 <= surah_number <= 114:
        raise HTTPException(status_code=400, detail="Номер суры должен быть от 1 до 114")
    
    try:
        async with httpx.AsyncClient() as client:
           
            response = await client.get(
                f"{QURAN_API_URL}/surah/{surah_number}/{edition}"
            )
            response.raise_for_status()
            return response.json()
    except httpx.HTTPStatusError as e:
        raise HTTPException(
            status_code=e.response.status_code,
            detail=f"Ошибка при получении суры: {str(e)}"
        )


async def get_ayah(surah_number: int, ayah_number: int, edition: Optional[str] = "ru.kuliev"):
   
    if not 1 <= surah_number <= 114:
        raise HTTPException(status_code=400, detail="Номер суры должен быть от 1 до 114")
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{QURAN_API_URL}/ayah/{surah_number}:{ayah_number}/{edition}"
            )
            response.raise_for_status()
            return response.json()
    except httpx.HTTPStatusError as e:
        raise HTTPException(
            status_code=e.response.status_code,
            detail=f"Ошибка при получении аята: {str(e)}"
        )