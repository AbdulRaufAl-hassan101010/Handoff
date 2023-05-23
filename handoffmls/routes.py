from flask import render_template, url_for, flash, redirect
from handoffmls import app, db
from handoffmls.forms import RegistrationForm, LoginForm
from handoffmls.models import Instituition, User
from flask_bcrypt import Bcrypt

# init bcrypt
bcrypt = Bcrypt(app)


@app.route("/")
@app.route("/home")
def home():
    return render_template("index.html")


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
        instituition =  Instituition.query.all()
        if  len(instituition) and bcrypt.check_password_hash(instituition[0].password, form.password.data):
            flash('You have been logged in!', 'success')
            return redirect(url_for('dashboard_home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/dashboard", methods=['GET', 'POST'])
def dashboard_home():
    return render_template("/dashboard/home.html")