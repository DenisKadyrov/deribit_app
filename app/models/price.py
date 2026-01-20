from sqlalchemy import BigInteger, Numeric, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Price(Base):
    __tablename__ = "prices"

    id: Mapped[int] = mapped_column(primary_key=True)
    ticker: Mapped[str] = mapped_column(String(10), index=True)
    price: Mapped[float] = mapped_column(Numeric(18, 8))
    ts: Mapped[int] = mapped_column(BigInteger, index=True)
