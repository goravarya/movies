from movies.models.movie import Movie
from movies.db import db


class MovieNotFoundException(Exception):
    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)


class MovieRepo:
    movie_id = None
    movie = None

    @staticmethod
    def get_all_movies():
        return Movie.query.filter(Movie.is_deleted == 0)

    @staticmethod
    def create_movie(name, director_name, release_year):
        new_movie = Movie(name, director_name, release_year)
        db.session.add(new_movie)
        db.session.commit()

        return new_movie

    def __init__(self, movie_id):
        self.movie_id = movie_id

    def get_movie(self):
        # If Movie object is not already loaded then load and cache for further use
        if not self.movie:
            self.movie = Movie.query.get(self.movie_id)

            # Raise exception if movie with the given id is not found
            if not self.movie:
                raise MovieNotFoundException('Movie with id {0} not found'.format(self.movie_id))

        return self.movie

    def update_movie(self, name, director_name, release_year):
        # Load move object
        movie = self.get_movie()

        # Update movie attributes
        movie.name = name
        movie.director_name = director_name
        movie.release_year = release_year

        # Persist the recent changes to DB
        db.session.commit()

        return movie

    def delete_movie(self):
        self.get_movie().is_deleted = True
        db.session.commit()
