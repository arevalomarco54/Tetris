from flask import Flask, render_template, redirect, url_for, flash
from wtforms.validators import DataRequired, Email, EqualTo
from forms import RegistrationForm, LoginForm
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = '63b1fed46dc9bcccc39ca2a9f86be2b1'
app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///site.db'
db = SQLAlchemy(app)

class User(db.Model):
    id= db.Column(db.Integer, primary_key = True)
    username= db.Column(db.String(20), unique=True, nullable=False)
    email= db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    games = db.relationship('Game', backref='player', lazy =True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

class Game(db.Model):
    id= db.Column(db.Integer, primary_key = True)
    date= db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    score = db.Column(db.Integer, nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    
    def __repr__(self):
        return f"Game:('{self.date}''{self.score}')"








@app.route("/")
@app.route("/home")
def home():
    return render_template('main.html', title='MA')


@app.route('/signup', methods = ['GET', 'POST'])
def signup():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    else:
        return render_template('signup.html', title = 'Sign Up', form = form)

@app.route('/login', methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    return render_template('login.html', form = form)


if __name__ == '__main__':
    app.run(debug=True)