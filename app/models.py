from typing import Optional, List
from datetime import datetime
import uuid
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Column, String, JSON, LargeBinary, Text

class TrustList(SQLModel, table=True):
    __tablename__ = "trustlist"
    uuid: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True, max_length=36)
    url: str = Field(sa_column=Column(Text, nullable=False))
    # Legacy field, kept for reference or backup, but we might migrate away from it.
    target_view_narray: Optional[bytes] = Field(default=None, sa_column=Column(LargeBinary().with_variant(LargeBinary(length=16777215), "mysql"), nullable=True))
    target_view_signature: Optional[str] = Field(default=None, sa_column=Column(Text, nullable=True))

    # New field for Deep Learning Embedding
    # Storing as JSON list of floats
    target_view_embedding: Optional[List[float]] = Field(default=None, sa_column=Column(JSON, nullable=True))

    domains: List["TrustDomain"] = Relationship(back_populates="trust_entry")

class TrustDomain(SQLModel, table=True):
    __tablename__ = "trust_domain"
    uuid: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True, max_length=36)
    foreign_key: str = Field(foreign_key="trustlist.uuid", max_length=36)
    domain: str = Field(sa_column=Column(Text, nullable=False))

    trust_entry: Optional[TrustList] = Relationship(back_populates="domains")

class BlackList(SQLModel, table=True):
    __tablename__ = "blacklist"
    uuid: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True, max_length=36)
    url: str = Field(sa_column=Column(Text, nullable=False))
    date: datetime = Field(default_factory=datetime.utcnow)
    url_hash: str = Field(unique=True, max_length=64)

class WarnList(SQLModel, table=True):
    __tablename__ = "warnlist"
    uuid: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True, max_length=36)
    url: str = Field(sa_column=Column(Text, nullable=False))
    origin: str = Field(sa_column=Column(Text, nullable=False))
    date: datetime = Field(default_factory=datetime.utcnow)

class ResultCache(SQLModel, table=True):
    __tablename__ = "result_cache"
    url_hash: str = Field(primary_key=True, max_length=64)
    score: float
