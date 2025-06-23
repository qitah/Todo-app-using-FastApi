from app.db.session import Base
from sqlalchemy import Column, String, Integer, ForeignKey, Boolean, DateTime
from sqlalchemy.orm import relationship
from app.models.users_model import shared_lists

class Todo(Base):
    __tablename__ = 'todo'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String, index=True)
    user_id = Column(Integer, ForeignKey("user.id"), unique=True)
    tasks = relationship('Task', cascade='all,delete', backref='todo')
    shared_with = relationship(
        "User",
        secondary=shared_lists,
        back_populates="shared_lists",
    )

class Task(Base):
    __tablename__ = 'task'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String, index=True)
    is_done = Column(Boolean, default=False)
    due_date = Column(DateTime, nullable=False)
    todo_id = Column(Integer, ForeignKey("todo.id"))