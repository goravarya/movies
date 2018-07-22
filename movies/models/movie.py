from movies.db import db
from sqlalchemy import Column, Integer, String, Boolean


class Movie(db.Model):
    __tablename__ = 'movies'

    movie_id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    director_name = Column(String, nullable=False)
    release_year = Column(Integer, nullable=False)
    is_deleted = Column(Boolean, nullable=False, default=False)

    def __init__(self, name, director_name, release_year):
        self.name = name
        self.director_name = director_name
        self.release_year = release_year
