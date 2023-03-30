#!/usr/bin/env python3

from app.db.crud import create_user
from app.db.schemas import UserCreate
from app.db.session import AsyncSessionLocal
import asyncio


async def init() -> None:
    db = AsyncSessionLocal()

    await create_user(
        db,
        UserCreate(
            email="admin@admin.com",
            password="adminadmin",
            is_active=True,
            is_superuser=True,
        ),
    )
    await db.close()


if __name__ == "__main__":
    print("Creating superuser admin@admin.com")
    asyncio.get_event_loop().run_until_complete(init())
    print("Superuser created")
