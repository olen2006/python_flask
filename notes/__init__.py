#https://flask.palletsprojects.com/en/1.1.x/patterns/appfactories/?highlight=application%20factory
####MAIN####https://flask.palletsprojects.com/en/1.0.x/tutorial/factory/
import os #get env vars
import functools
from flask import Flask, render_template, redirect, url_for,request, flash,session,g
#flask_migrate will create migrations for us
from flask_migrate import Migrate #to create tables in Db and make modifications to our class. Like add a column to our user class
from werkzeug.security import generate_password_hash, check_password_hash


def create_app(test_config=None):
    #create and config the App
    # NONE - In case we want to add in your own configuration if I want to do some automated testing against this web application
    app = Flask(__name__)
    app.config.from_mapping(
            SECRET_KEY=os.environ.get('SECRECT_KEY', default='dev')
            )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)#silent=True so it won't failed if file is not there.
    else:
        app.config.from_mapping(test_config)

    from .models import db, User, Note

    db.init_app(app)
    migrate = Migrate(app, db)
   #sign_up() - is a view function
    def require_login(view):
        #return a fun-n that decorates the view that you passed in
        #need it to map the meta data of the function back (we are adding special data to that decorated function)
        @functools.wraps(view)
        #catch any keyword arguments that comes in
        def wrapped_view(**kwargs):
            if not g.user:
                #you can't look up the notes unless you logged in
                return redirect(url_for('log_in'))
            return view(**kwargs)
        return wrapped_view
    #error handler
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404
    @app.before_request
    def load_user():
        user_id = session.get('user_id')
        if user_id:
            g.user = User.query.get(user_id)
        else:
            g.user = None

   # creating our 1st route
    @app.route('/sign_up', methods=('GET','POST'))
    def sign_up():
        # it will return rendered html template
        if request.method =='POST':
            username = request.form['username']
            password = request.form['password']
            error = None

            if not username:
                error = 'Username is required.'
            elif not password:
                error = 'Password is required.'
            #user class was inherited from db model so we habe some extra things on a class itself
            #we filter query to return only username
            #.first() means if there is a match in db
            elif User.query.filter_by(username=username).first():
                error = 'Username is already taken.'
            if error is None:
                user = User(username=username, password=generate_password_hash(password))
                db.session.add(user)
                db.session.commit()
                flash("Successfully signed up! Please log in.", 'success')
                return redirect(url_for('log_in'))

            flash(error, 'error')

        return render_template('sign_up.html')
    @app.route('/log_in', methods=('GET','POST'))
    def log_in():
        #regular check
         if request.method =='POST':
              username = request.form['username']
              password = request.form['password']
              error = None
              user = User.query.filter_by(username=username).first()
              #better user and password check should be added
              if not user or check_password_hash(user.password, password):
                  error = 'Username or password is incorrect.'
              if error is None:
                  session.clear()
                  session['user_id'] = user.id
                  return redirect(url_for('index'))
              flash(error,'error')
         return render_template('log_in.html')
    @app.route('/log_out', methods=('GET','DELETE'))
    def log_out():
        session.clear()
        flash('Successfully logged out.', 'success')
        return redirect(url_for('log_in'))
    @app.route('/')
    def index():
        return 'Index'
    #lising out notes
    @app.route('/notes')
    @require_login
    def note_index():
        return render_template('note_index.html', notes=g.user.notes)
    @app.route('/notes/new', methods=('GET','POST'))
    @require_login
    def note_create():
        if request.method =='POST':
              title = request.form['title']
              body = request.form['body']
              error = None

              if not title:
                  error = 'Title is required.'

              if error is None:
                  note = Note(author=g.user, title=title, body=body)
                  db.session.add(note)
                  db.session.commit()
                  flash(f"Successfully created note: {title}", 'success')
                  return redirect(url_for('note_index'))

              flash(error, 'error')
        return render_template('note_create.html')
    #Dynamic routing
    @app.route('/notes/<note_id>/edit', methods=('GET','PATCH','POST','PUT'))
    def note_update(note_id):
        note = Note.query.filter_by(user_id=g.user.id, id=note_id).first_or_404()

        if request.method in ['PATCH','POST','PUT']:
            title = request.form['title']
            body = request.form['body']
            error = None

            if not title:
                error = 'Title is required.'

            if error is None:
              note.title = title
              note.body = body
              db.session.add(note)
              db.session.commit()
              flash(f"Successfully updated note: {title}", 'success')
              return redirect(url_for('note_index'))


        return render_template('note_update.html', note=note)

    @app.route('/notes/<note_id>/delete', methods=('GET','DELETE'))
    @require_login
    def note_delete(note_id):
        note = Note.query.filter_by(user_id=g.user.id, id=note_id).first_or_404()
        db.session.delete(note)
        db.session.commit()
        flash(f"Successfully deleted note: '{note.title}'", 'success')
        return redirect(url_for('note_index'))

    return app
