from flask import render_template, request, redirect, abort, url_for
from movies import app, logger
from repositories.movie_repo import MovieRepo, MovieNotFoundException


@app.route('/', methods=['GET'])
@app.route('/home', methods=['GET'])
def index():
    """
    Renders the listing of the movies
    :return: Response
    """
    # TODO: Handle search
    return render_template('home.html', movies=MovieRepo.get_all_movies(), message=request.args.get('message'))


@app.route('/update_movie', methods=['GET'])
def update_movie():
    movie = None
    movie_id = request.args.get('movie_id')
    mode = 'create'
    title = 'Create New Movie'
    name = ''
    director_name = ''
    release_year = ''

    if movie_id:
        try:
            movie = MovieRepo(movie_id).get_movie()

        except MovieNotFoundException as ex:
            logger.error(ex.message)
            # If movie is not found then raise HTTP 404
            if not movie:
                abort(404)

        title = 'Update Movie'
        mode = 'update'

        name = movie.name
        director_name = movie.director_name
        release_year = movie.release_year

    return render_template('update_movie.html', values={
        'title': title,
        'mode': mode,
        'movie_id': movie_id,
        'name': name,
        'director_name': director_name,
        'release_year': release_year
    })


@app.route('/handle_create_update_movie', methods=['POST'])
def handle_create_update_movie():
    message = None
    try:
        # Get parm values from request
        mode = request.form.get('mode')
        movie_id = request.form.get('movie_id')
        name = request.form.get('name')
        director_name = request.form.get('director_name')
        release_year = request.form.get('release_year')

        # Create new movie record
        if mode == 'create':
            movie = MovieRepo.create_movie(
                name=name,
                director_name=director_name,
                release_year=release_year
            )
            message = 'Successfully created movie with id: {0}'.format(movie.movie_id)

        # Update existing movie record
        elif mode == 'update' and movie_id:
            MovieRepo(movie_id).update_movie(
                name=name,
                director_name=director_name,
                release_year=release_year
            )
            message = 'Successfully updated movie record'
        else:
            raise Exception('Invalid create/update request')

    except MovieNotFoundException as ex:
        logger.error(ex.message)
        raise Exception(ex.message)

    except Exception as ex:
        logger.error(ex.message)
        message = 'Error occurred! Unable to create/update movie.'

    return redirect(url_for('index', message=message))


@app.route('/delete_movie', methods=['GET'])
def delete_movie():
    """
    Handle request for movie deletion
    :return:
    """
    # FixMe: Delete request should ideally be submit via "Post" method
    message = None
    try:
        movie_id = request.args.get('movie_id')

        MovieRepo(movie_id).delete_movie()
        message = 'Successfully removed the movie'

    except MovieNotFoundException as ex:
        logger.error(ex.message)
        raise Exception(ex.message)

    except Exception as ex:
        logger.error(ex.message)
        message = 'Error occurred! Unable to delete movie.'

    return redirect(url_for('index', message=message))


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    print 'test'
    app.run()
