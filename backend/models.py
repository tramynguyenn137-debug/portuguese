from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Topic(Base):
    __tablename__ = "topics"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(String(255))
    icon = Column(String(10))
    words = relationship("Word", back_populates="topic")

class Word(Base):
    __tablename__ = "words"

    id = Column(Integer, primary_key=True, index=True)
    topic_id = Column(Integer, ForeignKey("topics.id"), nullable=False)
    portuguese = Column(String(200), nullable=False)
    vietnamese = Column(String(200), nullable=False)
    example_pt = Column(Text)
    example_vi = Column(Text)
    difficulty = Column(Integer, default=1)
    topic = relationship("Topic", back_populates="words")
