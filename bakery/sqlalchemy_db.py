from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Date, Time, func
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from datetime import datetime


from django.conf import settings

engine = create_engine(settings.DATABASE_URL)
Base = declarative_base()
Session = sessionmaker(bind=engine)

class ProductSQLAlchemy(Base):
    __tablename__ = 'bakery_product'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    time_to_cook = Column(Integer)


class OrderSQLAlchemy(Base):
    __tablename__ = 'bakery_order'

    id = Column(Integer, primary_key=True)
    person_name = Column(String)
    date = Column(Date, default=datetime.now().date())
    created_at = Column(Time, default=func.now())
    
    items = relationship("OrderItemSQLAlchemy", back_populates="order")

    def total_cook_time(self):
        total = sum(item.quantity * item.product.time_to_cook for item in self.items)
        return total
    
    def time_elapsed(self):
        created_at = self.created_at
        datetime_one = datetime.combine(datetime.today(), datetime.now().time())
        datetime_two = datetime.combine(self.date, created_at)
        return (datetime_one - datetime_two).total_seconds() / 60
    
    def cook_progress(self):
        total_time = self.total_cook_time()
        elapsed_time = self.time_elapsed()
        if total_time == 0:
            return 100
        progress = (elapsed_time / total_time) * 100
        return min(100, int(progress))


class OrderItemSQLAlchemy(Base):
    __tablename__ = 'bakery_orderitem'

    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey('bakery_order.id'))
    product_id = Column(Integer, ForeignKey('bakery_product.id'))
    quantity = Column(Integer)

    order = relationship("OrderSQLAlchemy", back_populates="items")
    product = relationship("ProductSQLAlchemy")
