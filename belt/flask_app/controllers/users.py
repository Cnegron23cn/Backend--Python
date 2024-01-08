from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.user import User
from flask_app.models.model_destinaton import Destination

from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:    #IF THE USER IS IN SESSION LOG IN, IF NOT LOG OUT
        return redirect('/logout')
    data ={ 'id':session['user_id']} #create a data to pass it in
    return render_template('dashboard.html', user = User.get_one(data),  plan= Destination.get_all())


@app.route('/register', methods=['POST'])
def register():
    if not User.validate_register(request.form): #CHECK IF USER IS IN FORM
        return redirect('/')       #IF NOT STAY ON  INDEX
    data = {                     #create a data to hash the password
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password":bcrypt.generate_password_hash(request.form['password']) #HASH PASSWORD HERE
    }
    id = User.create(data)  # SAVE IT and PUT USER ID INTO SESSION
    session['user_id'] = id #CREATE YOUR SESSION ID HERE
    return redirect('/dashboard')


@app.route('/login', methods=['POST'])
def login():
    user = User.get_by_email(request.form) #USER IS = TO THE EMAIL, IF NOT THE USER FLASH MSGS
    if not user:
        flash ('invalid email', 'login')
        return redirect ('/')
    if not bcrypt.check_password_hash(user.password, request.form['password']): #CHECK IF PASSWORD IS =
        flash ('invalid password', 'login')
        return redirect ('/')
    session['user_id'] = user.id #check if theyre stored in session
    return redirect ('/dashboard')

@app.route('/logout')
def home():
    session.clear()
    return redirect('/')