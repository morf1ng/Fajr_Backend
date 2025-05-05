from fastapi import FastAPI, HTTPException, Depends
from datetime import datetime
import psycopg2
from psycopg2.extras import RealDictCursor
from typing import Optional
from config import get_db_config, get_db_url
from contextlib import contextmanager

app = FastAPI()

# Контекстный менеджер для работы с БД
@contextmanager
def db_connection():
    config = get_db_config()
    conn = None
    try:
        conn = psycopg2.connect(
            host=config["host"],
            database=config["database"],
            user=config["user"],
            password=config["password"],
            port=config["port"],
            cursor_factory=RealDictCursor
        )
        yield conn
    except psycopg2.OperationalError as e:
        raise HTTPException(
            status_code=500,
            detail=f"Database connection error: {str(e)}"
        )
    finally:
        if conn:
            conn.close()

# Получение хадиса дня
@app.get("/hadith-of-the-day")
async def hadith_of_the_day():
    day_of_year = datetime.now().timetuple().tm_yday
    
    with db_connection() as conn:
        with conn.cursor() as cur:
            try:
                # Получаем общее количество хадисов
                cur.execute("SELECT COUNT(*) as count FROM hadiths")
                total_hadiths = cur.fetchone()['count']
                
                if total_hadiths == 0:
                    raise HTTPException(
                        status_code=404,
                        detail="No hadiths found in database"
                    )
                
                hadith_index = day_of_year % total_hadiths
                
                # Получаем хадис с информацией о книге и главе
                cur.execute("""
                    SELECT h.hadith_id, h.hadith_number, h.narrator, 
                           h.text, h.translation, h.grade,
                           c.title as chapter_title, c.chapter_number,
                           b.title as book_title, b.author
                    FROM hadiths h
                    JOIN chapters c ON h.chapter_id = c.chapter_id
                    JOIN books b ON c.book_id = b.book_id
                    ORDER BY h.hadith_id
                    LIMIT 1 OFFSET %s
                """, (hadith_index,))
                
                hadith = cur.fetchone()
                
                if not hadith:
                    raise HTTPException(
                        status_code=404,
                        detail="Hadith not found"
                    )
                    
                return {
                    "hadith": hadith,
                    "day_of_year": day_of_year,
                    "date": datetime.now().strftime("%Y-%m-%d")
                }
                
            except psycopg2.Error as e:
                raise HTTPException(
                    status_code=500,
                    detail=f"Database error: {str(e)}"
                )

# Дополнительные endpoint'ы (аналогично исправленные)
@app.get("/hadiths/{hadith_id}")
async def get_hadith(hadith_id: int):
    with db_connection() as conn:
        with conn.cursor() as cur:
            try:
                cur.execute("""
                    SELECT h.hadith_id, h.hadith_number, h.narrator, 
                           h.text, h.translation, h.grade,
                           c.title as chapter_title, c.chapter_number,
                           b.title as book_title, b.author
                    FROM hadiths h
                    JOIN chapters c ON h.chapter_id = c.chapter_id
                    JOIN books b ON c.book_id = b.book_id
                    WHERE h.hadith_id = %s
                """, (hadith_id,))
                
                hadith = cur.fetchone()
                
                if not hadith:
                    raise HTTPException(
                        status_code=404,
                        detail="Hadith not found"
                    )
                    
                return hadith
                
            except psycopg2.Error as e:
                raise HTTPException(
                    status_code=500,
                    detail=f"Database error: {str(e)}"
                )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)