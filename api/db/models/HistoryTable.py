from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, Double, ForeignKey
from api.db.decl_base import MainBase


class History(MainBase):
    """
    Object of History table
    """

    __tablename__ = "history_table"

    score: Mapped[int] = mapped_column(Integer)
    right_word: Mapped[int] = mapped_column(Integer)
    lose_word: Mapped[int] = mapped_column(Integer)
    procent_game: Mapped[float] = mapped_column(Double)

    #Foreign key
    user_id: Mapped[int] = mapped_column(ForeignKey("user_table.id", ondelete="CASCADE"))
    user: Mapped["User"] = relationship(back_populates="history")

    def __str__(self) -> str:
        return str(
            {
                
                f"{key}": value for key, value in self.__dict__.items()
            }
        )
    
    def __repr(self) -> str:
        return self.__str__()