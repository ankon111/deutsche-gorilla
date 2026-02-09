import random

from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.database import Base, engine, SessionLocal

WORDS = [
    ("Haus", "Noun", "das", "Häuser"),
    ("gehen", "Verb", None, None),
    ("schnell", "Adjective", None, None),
    ("lernen", "Verb", None, None),
    ("Buch", "Noun", "das", "Bücher"),
]

LEVELS = ["A1", "A2", "B1", "B2", "C1", "C2"]


def build_payload(index: int) -> schemas.WordCreate:
    base = random.choice(WORDS)
    word = f"{base[0]}_{index}"
    level = random.choice(LEVELS)
    translations = [
        schemas.TranslationCreate(language_code="en", meaning=f"English meaning {index}"),
        schemas.TranslationCreate(language_code="bn", meaning=f"Bangla meaning {index}"),
    ]
    examples = [
        schemas.ExampleCreate(sentence=f"Example sentence {index} A."),
        schemas.ExampleCreate(sentence=f"Example sentence {index} B."),
    ]
    conjugation = None
    if base[1] == "Verb":
        conjugation = schemas.VerbConjugationBase(
            praesens="ich ...",
            praeteritum="ich ...",
            perfekt="ich habe ...",
            imperativ="du ...",
        )
    return schemas.WordCreate(
        word=word,
        level=level,
        pos=base[1],
        article=base[2],
        plural=base[3],
        translations=translations,
        examples=examples,
        conjugation=conjugation,
    )


def main() -> None:
    Base.metadata.create_all(bind=engine)
    db: Session = SessionLocal()
    try:
        crud.ensure_parts_of_speech(db)
        for idx in range(1, 101):
            payload = build_payload(idx)
            crud.create_word(db, payload)
        print("Seeded 100 words.")
    finally:
        db.close()


if __name__ == "__main__":
    main()
