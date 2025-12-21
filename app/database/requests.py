from app.database.models import async_session, User, Category, DailyMetric, MoodRecord
from sqlalchemy import select, and_, func
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

async def save_mood_record(tg_id: int, mood_type: str, emoji: str):
    async with async_session() as session:
        user = await set_user(tg_id)
        today_str = date.today().isoformat()
        
        mood_record = MoodRecord(
            user_id=user.id,
            date=today_str,
            mood=mood_type,
            emoji=emoji
        )
        session.add(mood_record)
        await session.commit()
        return mood_record

async def get_mood_statistics(tg_id: int):
    async with async_session() as session:
        user = await set_user(tg_id)
        
        result = await session.execute(
            select(
                MoodRecord.mood,
                MoodRecord.emoji,
                func.count(MoodRecord.id).label('count')
            )
            .where(MoodRecord.user_id == user.id)
            .group_by(MoodRecord.mood, MoodRecord.emoji)
            .order_by(func.count(MoodRecord.id).desc())
        )
        
        stats = result.all()
        
        if not stats:
            return None
        
        total_count = sum(stat.count for stat in stats)
        return {
            'total': total_count,
            'stats': [
                {'mood': stat.mood, 'emoji': stat.emoji, 'count': stat.count}
                for stat in stats
            ],
            'most_common': {
                'mood': stats[0].mood,
                'emoji': stats[0].emoji,
                'count': stats[0].count
            }
        }

async def get_all_moods(tg_id: int):
    async with async_session() as session:
        user = await set_user(tg_id)
        
        result = await session.execute(
            select(MoodRecord)
            .where(MoodRecord.user_id == user.id)
            .order_by(MoodRecord.date.desc(), MoodRecord.id.desc())
        )
        
        moods = result.scalars().all()
        return [
            {
                'date': mood.date,
                'emoji': mood.emoji,
                'mood': mood.mood
            }
            for mood in moods
        ]