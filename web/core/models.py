from sqlalchemy import Column, Integer, String, MetaData, Text, ForeignKey, TIMESTAMP
from sqlalchemy.sql import func
from sqlalchemy.orm import declarative_base, relationship

metadata: MetaData = MetaData()

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, index=True)
    chat_id = Column(String(100), unique=True, index=True)

    messages = relationship("Message", back_populates="user")

    # orders = relationship("Order", back_populates="user")

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
    title = Column(Text, nullable=False, index=True)
    price = Column(Integer, nullable=False, index=True)
    count = Column(Integer, nullable=False)

    def __str__(self):
        return f"{self.id} {self.title}"

    def __repr__(self):
        return f"<Flower(id={self.id}, title={self.title})>"


# class Order(Base):
#     __tablename__ = 'order'
#
#     id = Column(Integer, primary_key=True, index=True)
#     user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
#     flower = Column(Integer, ManeToMany('flower.id'), nullable=False)
#
#     user = relationship("User", back_populates="orders")
#
#     def __str__(self):
#         return f"{self.id} {self.user}"
#
#     def __repr__(self):
#         return f"<Order(id={self.id}, user={self.user})>"
