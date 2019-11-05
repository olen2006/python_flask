from flask_sqlalchemy import SQLAlchemy
from mistune import markdown
###ToDo###
# 1. Create user class (for someone to sign in into our app)
# 2. Create Notes class. User will create it's own unique notes

#We need an instance of a DB
db = SQLAlchemy()
#we need to associate our db.instance with our application and get values from the app into db, such as db connection etc.
class User(db.Model):
    #inherit user from db.Model
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())
    notes = db.relationship('Note', backref='author', lazy=True)#one-to-many relationships, to access notes
    #note.author will give us a user. #lazy=true meains we'll access user instance first and only then make a query to see if there other notes.

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    body = db.Column(db.Text)#main content of the bod
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'), nullable=False)

    @property
    def body_html(self):
        return markdown(self.body)
