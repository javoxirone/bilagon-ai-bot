import os
from aiogram.enums import ParseMode
from fastapi import FastAPI, HTTPException
from aiogram import Bot
from dotenv import load_dotenv
from pydantic import BaseModel
from database.announcement import Announcement as AnnouncementDB

load_dotenv()

bot = Bot(token=os.getenv("BOT_TOKEN"), parse_mode=ParseMode.HTML)
app = FastAPI()

announcement_db = AnnouncementDB()


class AnnouncementCreate(BaseModel):
    users: int
    is_ad: bool = False
    image_url: str = None
    content: str


class AnnouncementUpdate(BaseModel):
    users: int = None
    is_ad: bool = None
    image_url: str = None
    content: str = None


@app.get('/api/v1/announcement/')
async def get_announcement_list():
    return announcement_db.get_announcement_list()


@app.post("/api/v1/announcement/create")
async def create_announcement(announcement_create: AnnouncementCreate):
    return announcement_db.create_announcement(
        announcement_create.users,
        announcement_create.is_ad,
        announcement_create.image_url,
        announcement_create.content,
    )


@app.get("/api/v1/announcement/{id}/")
async def get_announcement(id: int):
    result = announcement_db.get_announcement(id)
    if result:
        return result
    raise HTTPException(status_code=404, detail="Announcement not found")


@app.put("/api/v1/announcement/{id}/update")
async def update_announcement(id: int, announcement_update: AnnouncementUpdate):
    existing_announcement = announcement_db.get_announcement(id)
    if not existing_announcement:
        raise HTTPException(status_code=404, detail="Announcement not found")

    announcement_db.update_announcement(
        id,
        announcement_update.users,
        announcement_update.is_ad,
        announcement_update.image_url,
        announcement_update.content,
    )
    return {"message": "Announcement updated successfully"}


@app.delete("/api/v1/announcement/{id}/delete/")
async def delete_announcement(id: int):
    existing_announcement = announcement_db.get_announcement(id)
    if not existing_announcement:
        raise HTTPException(status_code=404, detail="Announcement not found")

    announcement_db.delete_announcement(id)
    return {"message": "Announcement deleted successfully"}
