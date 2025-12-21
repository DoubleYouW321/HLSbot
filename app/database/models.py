from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from sqlalchemy import BigInteger, ForeignKey, UniqueConstraint
from datetime import date

engine = create_async_engine(url='sqlite+aiosqlite:///db.sqlite3', echo=False)
async_session = async_sessionmaker(engine, expire_on_commit=False)

class Base(AsyncAttrs, DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id: Mapped[int] = mapped_column(BigInteger, unique=True)
    daily_metrics: Mapped[list["DailyMetric"]] = relationship(back_populates="user")
    category: Mapped["Category"] = relationship(back_populates="user")

class DailyMetric(Base):
    __tablename__ = 'daily_metrics'
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    date: Mapped[str] = mapped_column(default=lambda: date.today().isoformat())
    water_glasses: Mapped[int] = mapped_column(default=0)
    sleep_hours: Mapped[float] = mapped_column(default=0.0)
    steps: Mapped[int] = mapped_column(default=0)
    user: Mapped["User"] = relationship(back_populates="daily_metrics")
    __table_args__ = (UniqueConstraint('user_id', 'date', name='unique_user_date'),)

class Category(Base):
    __tablename__ = 'categories'
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    water: Mapped[int] = mapped_column(default=8)
    hours: Mapped[int] = mapped_column(default=8)
    steps: Mapped[int] = mapped_column(default=10000)
    user: Mapped["User"] = relationship(back_populates="category")

class MoodRecord(Base):
    __tablename__ = 'mood_records'
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    date: Mapped[str] = mapped_column(default=lambda: date.today().isoformat())
    mood: Mapped[str] = mapped_column()  
    emoji: Mapped[str] = mapped_column() 

async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)