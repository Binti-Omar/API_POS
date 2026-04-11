from sqlalchemy.orm import DeclarativeBase,Mapped,mapped_column
from sqlalchemy import String,Integer,Float,DateTime,ForeignKey
from datetime import datetime

class Base(DeclarativeBase):
    pass

class User((Base)):
    __tablename__='users'
    id:Mapped[int] = mapped_column(Integer,primary_key=True)
    full_name:Mapped[str] = mapped_column(String(200))
    email:Mapped[str] = mapped_column(String(100),unique=True)
    password:Mapped[str] = mapped_column(String(200))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

class Product((Base)):
    __tablename__='products'
    id:Mapped[int] = mapped_column(Integer,primary_key=True)
    user_id:Mapped[int] = mapped_column(ForeignKey('users.id'))
    name:Mapped[str] = mapped_column(String(200))
    amount:Mapped[Float] = mapped_column(Float)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

class Sales((Base)):
    __tablename__='sales'
    id:Mapped[int] = mapped_column(Integer,primary_key=True)
    product_id:Mapped[int] = mapped_column(ForeignKey('products.id'))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

class Payment(Base):
    __tablename__ = 'payments'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    sale_id: Mapped[int] = mapped_column(ForeignKey("sales.id"))
    trans_code: Mapped[str] = mapped_column(String(100))
    trans_amount: Mapped[float] = mapped_column(Float)
    phone_paid: Mapped[str] = mapped_column(String(20))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)



