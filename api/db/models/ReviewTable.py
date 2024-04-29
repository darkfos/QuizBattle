from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Text, Integer, ForeignKey
from api.db.decl_base import MainBase


class Review(MainBase):
    """
    Object of review table
    """

    __tablename__ = "review_table"

    message: Mapped[str] = mapped_column(Text)
    
    #Foreign key
    user_id: Mapped[int] = mapped_column(ForeignKey("user_table.id", ondelete="CASCADE"))
    user: Mapped["User"] = relationship(back_populates="reviews")

    def __str__(self) -> str:
        return str(
            {
                f"{key}": value for key, value in self.__dict__.items()
            }
        )
    
    def __repr__(self) -> str:
        return self.__str__()