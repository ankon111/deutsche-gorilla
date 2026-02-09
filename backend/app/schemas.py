from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, EmailStr


class TranslationBase(BaseModel):
    language_code: str
    meaning: str


class TranslationCreate(TranslationBase):
    pass


class Translation(TranslationBase):
    id: int

    class Config:
        from_attributes = True


class ExampleBase(BaseModel):
    sentence: str


class ExampleCreate(ExampleBase):
    pass


class Example(ExampleBase):
    id: int

    class Config:
        from_attributes = True


class VerbConjugationBase(BaseModel):
    praesens: str
    praeteritum: str
    perfekt: str
    imperativ: str


class VerbConjugation(VerbConjugationBase):
    id: int

    class Config:
        from_attributes = True


class WordBase(BaseModel):
    word: str
    level: Optional[str] = None
    pos: str
    article: Optional[str] = None
    plural: Optional[str] = None


class WordCreate(WordBase):
    translations: List[TranslationCreate]
    examples: List[ExampleCreate]
    conjugation: Optional[VerbConjugationBase] = None


class WordSummary(BaseModel):
    id: int
    word: str
    level: Optional[str]
    pos: str
    article: Optional[str]
    plural: Optional[str]
    translations: List[Translation]

    class Config:
        from_attributes = True


class WordDetail(WordSummary):
    examples: List[Example]
    conjugation: Optional[VerbConjugation]


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserSettings(BaseModel):
    default_mode: str
    daily_limit: int
    enabled_languages: str
    srs_enabled: bool
    preferred_ai_provider: str

    class Config:
        from_attributes = True


class UserProfile(BaseModel):
    id: int
    username: str
    email: EmailStr
    created_at: datetime
    settings: Optional[UserSettings]

    class Config:
        from_attributes = True


class ProgressUpdate(BaseModel):
    word_id: int
    learned: bool
    correct_delta: int = 0
    wrong_delta: int = 0


class GeneratedExamplesRequest(BaseModel):
    provider: str
    apiKey: str
    count: int = 2


class GeneratedExamplesResponse(BaseModel):
    examples: List[str]


class ChatRequest(BaseModel):
    provider: str
    apiKey: str
    message: str
    history: List[dict] = []
    word_id: Optional[int] = None


class ChatResponse(BaseModel):
    reply: str


class GrammarLesson(BaseModel):
    id: int
    level: str
    title: str
    content: str

    class Config:
        from_attributes = True
