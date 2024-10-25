from app.database.models import async_session , User, Data
from sqlalchemy import select, update, delete, values


async def set_user(tg_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        if not user:
            session.add(User(tg_id = tg_id))
            await session.commit()

async def register_user(name, age, number, tg_id):
    async with async_session() as session:
        data = await session.scalar(select(Data).where(Data.tg_id == tg_id))
        if not data:
            session.add(Data(name = name, age = age, number = number, tg_id = tg_id))
            await session.commit()
        else:
            data.name = name
            data.age = age
            data.number = number
            await session.commit()
