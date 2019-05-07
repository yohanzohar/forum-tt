from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///debat.db'
db = SQLAlchemy(app)
# migrate = Migrate (app,db)

class Discussion(db.Model):

	id = db.Column(db.Integer, primary_key = True)
	title = db.Column(db.Text)
	

class Message(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	text=db.Column(db.Text)
	user_id= db.Column(db.Integer, db.ForeignKey("user.id"), nullable = True)
	discussion_id = db.Column(db.Integer, db.ForeignKey("discussion.id"), nullable = True)
	


class User(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	username = db.Column(db.Text , unique=True , nullable=False)
	password = db.Column(db.Text,nullable=False)