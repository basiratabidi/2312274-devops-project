from sqlalchemy import Column, Integer, String
from .database import Base


class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    reg_no = Column(String, unique=True, nullable=False, index=True)
    name = Column(String, nullable=False)
    semester = Column(Integer, nullable=False)
    section = Column(String, nullable=False)
