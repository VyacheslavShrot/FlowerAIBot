from sqlalchemy import Column, Integer, String, MetaData, Text, ForeignKey, TIMESTAMP, Boolean, Float
from sqlalchemy.sql import func
from sqlalchemy.orm import declarative_base, relationship

metadata: MetaData = MetaData()

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, index=True)
    chat_id = Column(Integer, unique=True, index=True)
    admin = Column(Boolean, default=False, index=True)

    messages = relationship("Message", back_populates="user")

    orders = relationship("Order", back_populates="user")

    def __str__(self):
        return f"{self.id} {self.username}"

    def __repr__(self):
        return f"<User(id={self.id}, username={self.username})>"


class Message(Base):
    __tablename__ = 'message'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False, index=True)
    text = Column(Text, nullable=False)
    response = Column(Text, nullable=False)
    date = Column(TIMESTAMP, server_default=func.now(), nullable=False, index=True)

    user = relationship("User", back_populates="messages")

    def __str__(self):
        return f"{self.id} {self.user} {self.text[:10]}..."

    def __repr__(self):
        return f"<Message(id={self.id}, user={self.user}), text={self.text})>"


class Flower(Base):
    __tablename__ = 'flower'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False, index=True)
    price = Column(Float, nullable=False, index=True)
    count = Column(Integer, nullable=False)

    def __str__(self):
        return f"{self.id} {self.title}"

    def __repr__(self):
        return f"<Flower(id={self.id}, title={self.title})>"


class FlowerOrderAssociation(Base):
    __tablename__ = 'flower_order_association'

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey('order.id'), nullable=False)
    flower_id = Column(Integer, ForeignKey('flower.id'), nullable=False)
    count = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)

    flower = relationship("Flower")

    def __str__(self):
        return f"Order {self.order_id} - Flower {self.flower_id} (Count: {self.count})"

    def __repr__(self):
        return f"<FlowerOrderAssociation(order_id={self.order_id}, flower_id={self.flower_id}, count={self.count})>"


class Order(Base):
    __tablename__ = 'order'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    delivery_time = Column(String(100), nullable=False)

    flowers = relationship("FlowerOrderAssociation", backref="order", cascade="all, delete-orphan")

    user = relationship("User", back_populates="orders")

    def __str__(self):
        return f"{self.id} {self.user}"

    def __repr__(self):
        return f"<Order(id={self.id}, user={self.user})>"
