from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Optional
import random
import os

from database import get_db, engine
from models import Base, Topic, Word
from seed_data import seed

Base.metadata.create_all(bind=engine)
seed()

app = FastAPI(title="Portuguese Flashcard API")

ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "*").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/topics")
def get_topics(db: Session = Depends(get_db)):
    topics = db.query(Topic).all()
    result = []
    for t in topics:
        word_count = db.query(func.count(Word.id)).filter(Word.topic_id == t.id).scalar()
        result.append({
            "id": t.id,
            "name": t.name,
            "description": t.description,
            "icon": t.icon,
            "word_count": word_count,
        })
    return result

@app.get("/topics/{topic_id}")
def get_topic(topic_id: int, db: Session = Depends(get_db)):
    topic = db.query(Topic).filter(Topic.id == topic_id).first()
    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")
    word_count = db.query(func.count(Word.id)).filter(Word.topic_id == topic_id).scalar()
    return {
        "id": topic.id,
        "name": topic.name,
        "description": topic.description,
        "icon": topic.icon,
        "word_count": word_count,
    }

@app.get("/topics/{topic_id}/words")
def get_words_by_topic(topic_id: int, db: Session = Depends(get_db)):
    topic = db.query(Topic).filter(Topic.id == topic_id).first()
    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")
    words = db.query(Word).filter(Word.topic_id == topic_id).all()
    return [
        {
            "id": w.id,
            "topic_id": w.topic_id,
            "portuguese": w.portuguese,
            "vietnamese": w.vietnamese,
            "example_pt": w.example_pt,
            "example_vi": w.example_vi,
            "difficulty": w.difficulty,
        }
        for w in words
    ]

@app.get("/words/quiz")
def get_quiz_words(topic_id: Optional[int] = None, count: int = 10, db: Session = Depends(get_db)):
    query = db.query(Word)
    if topic_id:
        query = query.filter(Word.topic_id == topic_id)
    all_words = query.all()
    if len(all_words) < 4:
        raise HTTPException(status_code=400, detail="Not enough words for a quiz")
    quiz_words = random.sample(all_words, min(count, len(all_words)))
    result = []
    for correct in quiz_words:
        wrong_pool = [w for w in all_words if w.id != correct.id]
        wrong_choices = random.sample(wrong_pool, min(3, len(wrong_pool)))
        options = [correct.vietnamese] + [w.vietnamese for w in wrong_choices]
        random.shuffle(options)
        result.append({
            "id": correct.id,
            "portuguese": correct.portuguese,
            "correct_answer": correct.vietnamese,
            "options": options,
            "example_pt": correct.example_pt,
        })
    return result
