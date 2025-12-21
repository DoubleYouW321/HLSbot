from app.database.models import async_session, User, Category, DailyMetric
from sqlalchemy import select, and_
from datetime import date

async def set_user(tg_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        if not user:
            user = User(tg_id=tg_id)
            session.add(user)
            await session.flush()
            category = Category(user_id=user.id)
            session.add(category)
            await session.commit()
        return user

async def save_daily_metrics(tg_id: int, water: int, sleep: float, steps: int):
    async with async_session() as session:
        user = await set_user(tg_id)
        today_str = date.today().isoformat()
        
        metric = await session.scalar(
            select(DailyMetric).where(
                and_(DailyMetric.user_id == user.id, DailyMetric.date == today_str)
            )
        )
        
        if metric:
            metric.water_glasses = water
            metric.sleep_hours = sleep
            metric.steps = steps
        else:
            metric = DailyMetric(
                user_id=user.id,
                date=today_str,
                water_glasses=water,
                sleep_hours=sleep,
                steps=steps
            )
            session.add(metric)
        
        await session.commit()
        
        return {
            'water_glasses': water,
            'sleep_hours': sleep,
            'steps': steps,
            'date': today_str
        }

async def get_today_metrics(tg_id: int):
    async with async_session() as session:
        user = await set_user(tg_id)
        today_str = date.today().isoformat()
        
        metric = await session.scalar(
            select(DailyMetric).where(
                and_(DailyMetric.user_id == user.id, DailyMetric.date == today_str)
            )
        )
        
        if metric:
            return {
                'water_glasses': metric.water_glasses,
                'sleep_hours': metric.sleep_hours,
                'steps': metric.steps,
                'date': metric.date
            }
        return None

async def get_user_category(tg_id: int):
    async with async_session() as session:
        user = await set_user(tg_id)
        
        category = await session.scalar(
            select(Category).where(Category.user_id == user.id)
        )
        
        if category:
            return {
                'water': category.water,
                'hours': category.hours,
                'steps': category.steps
            }
        return None