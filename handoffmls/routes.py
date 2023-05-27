from functools import wraps
from flask import render_template, url_for, flash, redirect, session
from handoffmls import app, db
from handoffmls.forms import RegistrationForm, LoginForm
from handoffmls.models import Instituition, User
from flask_bcrypt import Bcrypt

from  handoffmls.middlewares import authentication_required

# init bcrypt
bcrypt = Bcrypt(app)




@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html")


@app.route("/about")
def about():
    return render_template('about.html', title='About')

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        instituition = Instituition(name=form.name.data, email=form.email.data, password=hashed_password)
        db.session.add(instituition)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        
        instituition =  Instituition.query.filter_by(email=email).first()
        if  instituition and bcrypt.check_password_hash(instituition.password, password):
            flash('You have been logged in!', 'success')
            # set session 
            session['user_id']= instituition.id
            session['username']= instituition.name
            print(session)
            return redirect(url_for('dashboard_home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/dashboard", methods=['GET', 'POST'])
@authentication_required
def dashboard_home(): 
    username = session.get('username')     
    return render_template('dashboard/home.html', username=username)


@app.route("/logout", methods=['GET', 'POST'])
def logout():
    session.clear()
    print(session)
    flash('You have been logged out', 'danger')
    return redirect(url_for('login'))   