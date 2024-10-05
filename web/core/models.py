from sqlalchemy import Column, Integer, String, MetaData, Text, ForeignKey, TIMESTAMP
from sqlalchemy.sql import func
from sqlalchemy.orm import declarative_base, relationship

metadata: MetaData = MetaData()

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, index=True)
    chat_id = Column(String(100), unique=True)

    messages = relationship("Message", back_populates="user")

    def __str__(self):
        return f"{self.id} {self.username}"

    def __repr__(self):
        return f"<User(id={self.id}, username={self.username})>"


class Message(Base):
    __tablename__ = 'message'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    text = Column(Text, nullable=False)
    response = Column(Text, nullable=False)
    date = Column(TIMESTAMP, server_default=func.now(), nullable=False)

    user = relationship("User", back_populates="messages")

    def __str__(self):
        return f"{self.id} {self.user} {self.text[:10]}..."

    def __repr__(self):
        return f"<Message(id={self.id}, user={self.user}), text={self.text})>"
