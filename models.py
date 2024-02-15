from typing import List
from datetime import datetime
from typing import Literal, Optional, get_args
from sqlalchemy import Column, Enum, Table
from sqlalchemy import String, Text
from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship


class Base(DeclarativeBase):
    pass


movies_actors = Table(
    "movies_actors",
    Base.metadata,
    Column('movie_id', ForeignKey("movies.id")),
    Column('person_id', ForeignKey("persons.id")),
)

movies_screenwriters = Table(
    "movies_screenwriters",
    Base.metadata,
    Column('movie_id', ForeignKey("movies.id")),
    Column('person_id', ForeignKey("persons.id")),
)

movies_directors = Table(
    "movies_directors",
    Base.metadata,
    Column('movie_id', ForeignKey("movies.id")),
    Column('person_id', ForeignKey("persons.id")),
)

movies_composers = Table(
    "movies_composers",
    Base.metadata,
    Column('movie_id', ForeignKey("movies.id")),
    Column('person_id', ForeignKey("persons.id")),
)

movies_operators = Table(
    "movies_operators",
    Base.metadata,
    Column('movie_id', ForeignKey("movies.id")),
    Column('person_id', ForeignKey("persons.id")),
)

movies_artists = Table(
    "movies_artists",
    Base.metadata,
    Column('movie_id', ForeignKey("movies.id")),
    Column('person_id', ForeignKey("persons.id")),
)


class Country(Base):
    __tablename__ = "countries"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))

    persons: Mapped[List['Person']] = relationship(back_populates="countries")
    movies: Mapped[List['Movie']] = relationship(back_populates="countries")


class Genre(Base):
    __tablename__ = "genres"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    movie_id: Mapped[int] = mapped_column(ForeignKey("movies.id"))
    person_id: Mapped[int] = mapped_column(ForeignKey("persons.id"))

    movies: Mapped[List['Movie']] = relationship(back_populates="genres")
    persons: Mapped[List['Person']] = relationship(back_populates="genres")


class Role(Base):
    __tablename__ = "roles"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    perons_id: Mapped[int] = mapped_column(ForeignKey("persons.id"))

    persons: Mapped[List['Person']] = relationship(back_populates="roles")


class Person(Base):
    __tablename__ = "persons"

    id: Mapped[int] = mapped_column(primary_key=True)
    full_name: Mapped[str] = mapped_column(String(250))
    birth_date: Mapped[datetime]
    country_id: Mapped[int] = mapped_column(ForeignKey("countries.id"))

    genres: Mapped[List['Genre']] = relationship(back_populates='persons')
    movies: Mapped[List['Movie']] = relationship(back_populates='persons')
    roles: Mapped[List['Role']] = relationship(back_populates='persons')
    countriy: Mapped['Country'] = relationship(back_populates="persons")


class Movie(Base):
    __tablename__ = "movies"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100))
    country_id: Mapped[int] = mapped_column(ForeignKey("countries.id"))
    year: Mapped[Optional[int]]
    premier_date: Mapped[Optional[datetime]]
    duration_min: Mapped[int] = mapped_column(default=0)
    description: Mapped[str] = mapped_column(Text())
    rate: Mapped[float] = mapped_column(default=0.0)

    country: Mapped['Country'] = relationship(back_populates="movies")
    genres: Mapped[List['Genre']] = relationship(back_populates="movies")
    reviews: Mapped[List['Review']] = relationship(back_populates="movies")
    screenwriters: Mapped[List['Person']] = relationship(
        secondary=movies_screenwriters)
    directors: Mapped[List['Person']] = relationship(
        secondary=movies_directors)
    composers: Mapped[List['Person']] = relationship(
        secondary=movies_composers)
    operators: Mapped[List['Person']] = relationship(
        secondary=movies_operators)
    artists: Mapped[List['Person']] = relationship(secondary=movies_artists)
    actors: Mapped[List['Person']] = relationship(secondary=movies_actors)


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(20), unique=True)
    email: Mapped[str] = mapped_column(String(20), unique=True)
    hash: Mapped[str] = mapped_column(String())
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow())
    updated_at: Mapped[datetime] = mapped_column(default=datetime.utcnow())

    reviews: Mapped[List['Review']] = relationship(back_populates="users")


ReviewTypes = Literal[
    "negative",
    "positive",
    "neutral",
]


class Review(Base):
    __tablename__ = "reviews"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100))
    body: Mapped[str] = mapped_column(Text())
    movie_id: Mapped[int] = mapped_column(ForeignKey("movies.id"))
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    type: Mapped[ReviewTypes] = mapped_column(Enum(
        *get_args(ReviewTypes),
        name="review_types",
        create_constraint=True,
        validate_strings=True,
    ))
    likes: Mapped[int] = mapped_column(default=0)
    dislikes: Mapped[int] = mapped_column(default=0)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow())
    updated_at: Mapped[datetime] = mapped_column(default=datetime.utcnow())

    movie: Mapped['Movie'] = relationship(back_populates="reviews")
    author: Mapped['User'] = relationship(back_populates="reviews")
