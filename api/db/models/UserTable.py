from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, BigInteger
from db.decl_base import MainBase
from datetime import datetime
from typing import List


class User(MainBase):
    """
    Object of user table
    """

    __tablename__ = "user_table"

    telegram_id: Mapped[int] = mapped_column(BigInteger)
    name_user: Mapped[str] = mapped_column(String(500))
    score: Mapped[int] = mapped_column(Integer)
    date_create: datetime
    date_update: datetime

    #Link with History
    history: Mapped["History"] = relationship(back_populates="user")

    #Link with all reviews
    reviews: Mapped[List["Review"]] = relationship(back_populates="user")

    def __str__(self) -> str:
        return str(
            {
                f"{key}": value
                for key, value in self.__dict__.items()
            }
        )
    
    def __repr__(self) -> str:
        return self.__str__()