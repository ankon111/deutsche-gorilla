from datetime import datetime
from typing import List, Optional

from sqlalchemy.orm import Session

from app import models, schemas


DEFAULT_POS = ["Noun", "Verb", "Adjective", "Adverb", "Pronoun", "Preposition", "Conjunction"]


def ensure_parts_of_speech(db: Session) -> None:
    existing = {pos.name for pos in db.query(models.PartOfSpeech).all()}
    for name in DEFAULT_POS:
        if name not in existing:
            db.add(models.PartOfSpeech(name=name))
    db.commit()


def get_pos(db: Session, name: str) -> models.PartOfSpeech:
    pos = db.query(models.PartOfSpeech).filter(models.PartOfSpeech.name == name).first()
    if not pos:
        pos = models.PartOfSpeech(name=name)
        db.add(pos)
        db.commit()
        db.refresh(pos)
    return pos


def create_word(db: Session, payload: schemas.WordCreate) -> models.Word:
    pos = get_pos(db, payload.pos)
    word = models.Word(
        word=payload.word,
        level=payload.level,
        pos_id=pos.id,
        article=payload.article,
        plural=payload.plural,
    )
    db.add(word)
    db.flush()

    for translation in payload.translations:
        db.add(models.Translation(word_id=word.id, **translation.dict()))
    for example in payload.examples:
        db.add(models.Example(word_id=word.id, sentence=example.sentence))
    if payload.conjugation:
        db.add(models.VerbConjugation(word_id=word.id, **payload.conjugation.dict()))

    db.commit()
    db.refresh(word)
    return word


def list_words(
    db: Session,
    search: Optional[str],
    pos: Optional[str],
    level: Optional[str],
    page: int,
    limit: int,
) -> List[models.Word]:
    query = db.query(models.Word)
    if search:
        query = query.filter(models.Word.word.ilike(f"%{search}%"))
    if level:
        query = query.filter(models.Word.level == level)
    if pos:
        query = query.join(models.PartOfSpeech).filter(models.PartOfSpeech.name == pos)
    return query.order_by(models.Word.word).offset((page - 1) * limit).limit(limit).all()


def get_word(db: Session, word_id: int) -> Optional[models.Word]:
    return db.query(models.Word).filter(models.Word.id == word_id).first()


def update_progress(db: Session, user_id: int, update: schemas.ProgressUpdate) -> models.UserProgress:
    progress = (
        db.query(models.UserProgress)
        .filter(models.UserProgress.user_id == user_id, models.UserProgress.word_id == update.word_id)
        .first()
    )
    if not progress:
        progress = models.UserProgress(user_id=user_id, word_id=update.word_id)
        db.add(progress)
    progress.learned = update.learned
    progress.correct_count += update.correct_delta
    progress.wrong_count += update.wrong_delta
    progress.last_seen = datetime.utcnow()
    db.commit()
    db.refresh(progress)
    return progress
