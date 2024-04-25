from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class MainBase(DeclarativeBase):
    """
    Main base for other tables
    """

    id: Mapped[int] = mapped_column(primary_key=True)