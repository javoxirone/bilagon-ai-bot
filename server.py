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


class AnnouncementCreate(BaseModel):
    telegram_id: int = None
    is_ad: bool = False
    image_url: str = None
    content: str = None


class AnnouncementUpdate(BaseModel):
    telegram_id: int = None
    telegram_message_id: int = None
    is_ad: bool = None
    image_url: str = None
    content: str = None


@app.get('/api/v1/announcement/')
async def get_announcement_list():
    announcement_db = AnnouncementDB()
    announcements = announcement_db.get_announcements()
    announcement_db.close()
    print(announcements)
    return announcements


@app.post("/api/v1/announcement/create")
async def create_announcement(announcement_create: AnnouncementCreate):
    telegram_message = await bot.send_message(announcement_create.telegram_id, announcement_create.content)
    announcement_db = AnnouncementDB()
    announcement_id = announcement_db.create_announcement(
        announcement_create.telegram_id,
        telegram_message.message_id,
        announcement_create.is_ad,
        announcement_create.image_url,
        announcement_create.content
    )
    announcement_db.close()
    return announcement_id


@app.get("/api/v1/announcement/{id}/")
async def get_announcement(id: int):
    announcement_db = AnnouncementDB()
    result = announcement_db.get_announcement(id)
    announcement_db.close()
    if result:
        return result
    raise HTTPException(status_code=404, detail="Announcement not found")


@app.put("/api/v1/announcement/{id}/update")
async def update_announcement(id: int, announcement_update: AnnouncementUpdate):
    announcement_db = AnnouncementDB()
    existing_announcement = announcement_db.get_announcement(id)
    announcement_db.close()
    if not existing_announcement:
        raise HTTPException(status_code=404, detail="Announcement not found")
    await bot.edit_message_text(announcement_update.content, announcement_update.telegram_id,
                                announcement_update.telegram_message_id)
    announcement_db = AnnouncementDB()
    announcement_db.update_announcement(
        id,
        announcement_update.is_ad,
        announcement_update.image_url,
        announcement_update.content,
    )
    announcement_db.close()
    return {"message": "Announcement updated successfully"}


@app.delete("/api/v1/announcement/{id}/delete/")
async def delete_announcement(id: int):
    announcement_db = AnnouncementDB()
    existing_announcement = announcement_db.get_announcement(id)
    announcement_db.close()
    if not existing_announcement:
        raise HTTPException(status_code=404, detail="Announcement not found")
    await bot.delete_message(existing_announcement["telegram_id"], existing_announcement["telegram_message_id"])
    announcement_db = AnnouncementDB()
    announcement_db.delete_announcement(id)
    announcement_db.close()
    return {"message": "Announcement deleted successfully"}
