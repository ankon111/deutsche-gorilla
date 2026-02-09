import logging
from typing import List, Optional

from fastapi import Depends, FastAPI, HTTPException, Query
from sqlalchemy.orm import Session

from app import auth, crud, models, schemas
from app.ai.providers import provider_factory
from app.database import Base, engine, get_db
from app.logging_config import configure_logging

configure_logging()
logger = logging.getLogger("deutschgorilla")

Base.metadata.create_all(bind=engine)

app = FastAPI(title="DeutschGorilla API")


@app.on_event("startup")
def seed_defaults() -> None:
    logger.info("Ensuring default parts of speech exist.")
    db = next(get_db())
    try:
        crud.ensure_parts_of_speech(db)
    finally:
        db.close()


@app.post("/api/auth/register", response_model=schemas.UserProfile)
def register_user(payload: schemas.UserCreate, db: Session = Depends(get_db)):
    if db.query(models.User).filter(models.User.username == payload.username).first():
        raise HTTPException(status_code=400, detail="Username already exists")
    if db.query(models.User).filter(models.User.email == payload.email).first():
        raise HTTPException(status_code=400, detail="Email already exists")

    user = models.User(
        username=payload.username,
        email=payload.email,
        password_hash=auth.hash_password(payload.password),
    )
    db.add(user)
    db.flush()
    settings = models.UserSettings(user_id=user.id)
    db.add(settings)
    db.commit()
    db.refresh(user)
    logger.info("User registered", extra={"username": user.username})
    return user


@app.post("/api/auth/login", response_model=schemas.Token)
def login_user(payload: schemas.UserLogin, db: Session = Depends(get_db)):
    user = auth.authenticate_user(db, payload.username, payload.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = auth.create_access_token(str(user.id))
    logger.info("User logged in", extra={"username": user.username})
    return schemas.Token(access_token=token)


@app.get("/api/words", response_model=List[schemas.WordSummary])
def list_words(
    search: Optional[str] = None,
    pos: Optional[str] = None,
    level: Optional[str] = None,
    page: int = Query(1, ge=1),
    limit: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db),
):
    words = crud.list_words(db, search, pos, level, page, limit)
    return [
        schemas.WordSummary(
            id=word.id,
            word=word.word,
            level=word.level,
            pos=word.pos.name,
            article=word.article,
            plural=word.plural,
            translations=word.translations,
        )
        for word in words
    ]


@app.get("/api/words/{word_id}", response_model=schemas.WordDetail)
def get_word(word_id: int, db: Session = Depends(get_db)):
    word = crud.get_word(db, word_id)
    if not word:
        raise HTTPException(status_code=404, detail="Word not found")
    return schemas.WordDetail(
        id=word.id,
        word=word.word,
        level=word.level,
        pos=word.pos.name,
        article=word.article,
        plural=word.plural,
        translations=word.translations,
        examples=word.examples,
        conjugation=word.conjugation,
    )


@app.post("/api/progress/update")
def update_progress(payload: schemas.ProgressUpdate, db: Session = Depends(get_db)):
    progress = crud.update_progress(db, user_id=1, update=payload)
    logger.info("Progress updated", extra={"word_id": progress.word_id})
    return {"status": "ok"}


@app.post("/api/words/{word_id}/examples/generate", response_model=schemas.GeneratedExamplesResponse)
def generate_examples(
    word_id: int,
    payload: schemas.GeneratedExamplesRequest,
    db: Session = Depends(get_db),
):
    word = crud.get_word(db, word_id)
    if not word:
        raise HTTPException(status_code=404, detail="Word not found")
    provider = provider_factory(payload.provider, payload.apiKey)
    examples = provider.generate_examples(word.word, payload.count)
    logger.info("Generated examples", extra={"word_id": word_id, "provider": payload.provider})
    return schemas.GeneratedExamplesResponse(examples=examples)


@app.post("/api/chat/word", response_model=schemas.ChatResponse)
def chat_word(payload: schemas.ChatRequest, db: Session = Depends(get_db)):
    context = None
    if payload.word_id:
        word = crud.get_word(db, payload.word_id)
        if not word:
            raise HTTPException(status_code=404, detail="Word not found")
        context = {"word": word.word, "pos": word.pos.name}
    provider = provider_factory(payload.provider, payload.apiKey)
    reply = provider.chat(payload.message, payload.history, context)
    logger.info("Word chat", extra={"provider": payload.provider})
    return schemas.ChatResponse(reply=reply)


@app.post("/api/chat/general", response_model=schemas.ChatResponse)
def chat_general(payload: schemas.ChatRequest):
    provider = provider_factory(payload.provider, payload.apiKey)
    reply = provider.chat(payload.message, payload.history, None)
    logger.info("General chat", extra={"provider": payload.provider})
    return schemas.ChatResponse(reply=reply)


@app.get("/api/grammar", response_model=List[schemas.GrammarLesson])
def list_grammar(level: Optional[str] = None, db: Session = Depends(get_db)):
    query = db.query(models.GrammarLesson)
    if level:
        query = query.filter(models.GrammarLesson.level == level)
    lessons = query.order_by(models.GrammarLesson.title).all()
    return lessons
