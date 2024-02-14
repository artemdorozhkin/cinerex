from ast import List
from datetime import datetime
from enum import Enum
from typing import Optional
from sqlalchemy import String
from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship


class Base(DeclarativeBase):
    pass


# TODO: check relations
# TODO: add association tables(https://docs.sqlalchemy.org/en/20/orm/basic_relationships.html#many-to-many) for:
# MoviesPersons
#     - id
#     - movie_id
#     - person_id
#     - role_id
# MoviesGenres
#     - id
#     - movie_id
#     - genre_id
# PersonsGenres
#     - id
#     - person_id
#     - genre_id

class Country(Base):
    __tablename__ = "countries"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))

    persons: Mapped[List['Person']] = relationship(back_populates='countries')


class Genre(Base):
    __tablename__ = "genres"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))


class Role(Base):
    __tablename__ = "roles"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))


class Person(Base):
    __tablename__ = "persons"

    id: Mapped[int] = mapped_column(primary_key=True)
    full_name: Mapped[str] = mapped_column(String(250))
    birth_date: Mapped[datetime]
    country_id: Mapped[int] = mapped_column(ForeignKey("contries.id"))

    genres: Mapped[List['Genre']] = relationship(
        back_populates='persons', cascade="all, delete-orphan")
    movies: Mapped[List['Movie']] = relationship(
        back_populates='persons', cascade="all, delete-orphan")

    countriy: Mapped["Country"] = relationship(back_populates="persons")


class Movie(Base):
    __tablename__ = "movies"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column()
    country_id: Mapped[int] = mapped_column()
    year: Mapped[Optional[int]]
    genre_id: Mapped[int] = mapped_column()
    screenwriter_id: Mapped[int] = mapped_column()
    director_id: Mapped[int] = mapped_column()
    composer_id: Mapped[int] = mapped_column()
    operator_id: Mapped[int] = mapped_column()
    artist_id: Mapped[int] = mapped_column()
    actor_id: Mapped[int] = mapped_column()
    premier_date: Mapped[str] = mapped_column()
    duration_min: Mapped[int] = mapped_column()
    description: Mapped[str] = mapped_column()
    rate: Mapped[float] = mapped_column()
    review_id: Mapped[int] = mapped_column()

    country: Mapped[List['Country']] = relationship(back_populates="movies")
    genres: Mapped[List['Genre']] = relationship(back_populates="movies")
    screenwriters: Mapped[List['Person']] = relationship(
        back_populates="movies")
    directors: Mapped[List['Person']] = relationship(back_populates="movies")
    composers: Mapped[List['Person']] = relationship(back_populates="movies")
    operators: Mapped[List['Person']] = relationship(back_populates="movies")
    artists: Mapped[List['Person']] = relationship(back_populates="movies")
    actors: Mapped[List['Person']] = relationship(back_populates="movies")
    reviews: Mapped[List['Review']] = relationship(back_populates="movies")


class ReviewTypes(Enum):
    negative = "negative"
    positive = "positive"
    neutral = "neutral"


class Review(Base):
    __tablename__ = "reviews"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    body: Mapped[str]
    movie: Mapped['Movie']
    author: Mapped['User']
    type: Mapped['ReviewTypes']
    likes: Mapped[int]
    dislikes: Mapped[int]
    created_at: Mapped[datetime]
    updated_at: Mapped[datetime]


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str]
    email: Mapped[str]
    hash: Mapped[str]
    reviews: Mapped[List['Review']]
    created_at: Mapped[datetime]
    updated_at: Mapped[datetime]
