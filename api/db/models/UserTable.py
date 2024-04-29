from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, BigInteger, Date, LargeBinary
from sqlalchemy.sql import func
from api.db.decl_base import MainBase
from datetime import datetime
from typing import List


class User(MainBase):
    """
    Object of user table
    """

    __tablename__ = "user_table"

    telegram_id: Mapped[int] = mapped_column(BigInteger, nullable=False, unique=True)
    name_user: Mapped[str] = mapped_column(String(500))
    photo: Mapped[bytes] = mapped_column(LargeBinary, nullable=True)
    score: Mapped[int] = mapped_column(Integer)
    game_count: Mapped[int] = mapped_column(Integer, nullable=True)
    date_create: Mapped[datetime] = mapped_column(Date)
    date_update: Mapped[datetime] = mapped_column(Date)

    #Link with History
    history: Mapped[List["History"]] = relationship(back_populates="user", cascade='save-update, merge, delete',
        passive_deletes=True)

    #Link with all reviews
    reviews: Mapped[List["Review"]] = relationship(back_populates="user", cascade='save-update, merge, delete',
        passive_deletes=True)

    def __str__(self) -> str:
        return str(
            {
                f"{key}": value
                for key, value in self.__dict__.items()
            }
        )
    
    def __repr__(self) -> str:
        return self.__str__()