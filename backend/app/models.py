from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import relationship

from app.database import Base


class PartOfSpeech(Base):
    __tablename__ = "parts_of_speech"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)


class Word(Base):
    __tablename__ = "words"

    id = Column(Integer, primary_key=True, index=True)
    word = Column(String, nullable=False, unique=True)
    level = Column(String, nullable=True)
    pos_id = Column(Integer, ForeignKey("parts_of_speech.id"), nullable=False)
    article = Column(String, nullable=True)
    plural = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    pos = relationship("PartOfSpeech")
    translations = relationship("Translation", cascade="all, delete-orphan")
    examples = relationship("Example", cascade="all, delete-orphan")
    conjugation = relationship("VerbConjugation", uselist=False, cascade="all, delete-orphan")


class Translation(Base):
    __tablename__ = "translations"

    id = Column(Integer, primary_key=True, index=True)
    word_id = Column(Integer, ForeignKey("words.id", ondelete="CASCADE"), nullable=False)
    language_code = Column(String, nullable=False)
    meaning = Column(String, nullable=False)

    __table_args__ = (UniqueConstraint("word_id", "language_code", name="uix_word_language"),)


class Example(Base):
    __tablename__ = "examples"

    id = Column(Integer, primary_key=True, index=True)
    word_id = Column(Integer, ForeignKey("words.id", ondelete="CASCADE"), nullable=False)
    sentence = Column(Text, nullable=False)


class VerbConjugation(Base):
    __tablename__ = "verb_conjugations"

    id = Column(Integer, primary_key=True, index=True)
    word_id = Column(Integer, ForeignKey("words.id", ondelete="CASCADE"), unique=True, nullable=False)
    praesens = Column(Text, nullable=False)
    praeteritum = Column(Text, nullable=False)
    perfekt = Column(Text, nullable=False)
    imperativ = Column(Text, nullable=False)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=False, unique=True)
    password_hash = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    settings = relationship("UserSettings", uselist=False, cascade="all, delete-orphan")


class UserSettings(Base):
    __tablename__ = "user_settings"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    default_mode = Column(String, default="flashcards")
    daily_limit = Column(Integer, default=20)
    enabled_languages = Column(Text, default='["bn","en"]')
    srs_enabled = Column(Boolean, default=False)
    preferred_ai_provider = Column(String, default="openai")


class UserProgress(Base):
    __tablename__ = "user_progress"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    word_id = Column(Integer, ForeignKey("words.id", ondelete="CASCADE"), nullable=False)
    learned = Column(Boolean, default=False)
    last_seen = Column(DateTime, nullable=True)
    correct_count = Column(Integer, default=0)
    wrong_count = Column(Integer, default=0)

    __table_args__ = (UniqueConstraint("user_id", "word_id", name="uix_user_word"),)


class GrammarLesson(Base):
    __tablename__ = "grammar_lessons"

    id = Column(Integer, primary_key=True, index=True)
    level = Column(String, nullable=False)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
