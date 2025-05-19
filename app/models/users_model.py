from datetime import datetime, timezone
from app.db.session import Base
from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, Table
from sqlalchemy.orm import relationship

shared_lists = Table(
    "shared_lists",
    Base.metadata,
    Column("user_id", ForeignKey("user.id"), primary_key=True),
    Column("todo_id", ForeignKey("todo.id"), primary_key=True),
)

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))
    todo = relationship('Todo', cascade='all,delete', backref='user')
    shared_lists = relationship("Todo", secondary=shared_lists, back_populates='shared_with')

