from flask import render_template, url_for, flash, redirect, session
from handoffmls import app, db
from handoffmls.forms import RegistrationForm, LoginForm
from handoffmls.models.lab import Lab
from handoffmls.models.user import User
from flask_bcrypt import Bcrypt
from handoffmls.landingpage import landingpage

from handoffmls.middlewares import is_logged_in

# init bcrypt
bcrypt = Bcrypt(app)


@landingpage.route("/")
@landingpage.route("/home")
@is_logged_in
def home():
    total_users = len(User.query.all())
    total_labs = len(Lab.query.all())
    return render_template("home.html", total_users=total_users, total_labs=total_labs, title="Handoff")


@landingpage.route("/about")
def about():
    return render_template('landingpage.about.html', title='About')


@landingpage.route("/register", methods=['GET', 'POST'])
@is_logged_in
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        lab = Lab(name=form.name.data, email=form.email.data,
                  password=hashed_password)
        db.session.add(lab)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('landingpage.login'))
    return render_template('register.html', title='Register', form=form)


@landingpage.route("/login", methods=['GET', 'POST'])
@is_logged_in
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        lab = Lab.query.filter_by(email=email).first()
        if lab and bcrypt.check_password_hash(lab.password, password):
            # set session
            session['lab_id'] = lab.id
            session['username'] = lab.name
            return redirect(url_for('dashboard.dashboard_home'))

        user = User.query.filter_by(email=email).first()
        # if  (user and bcrypt.check_password_hash(user.password, password)) and user.password == 'password':
        print(user)
        if user and user.password == password:
            # clear sessions
            session.clear()

            # set session
            session['user_id'] = user.id
            session['username'] = f"{user.last_name}"
            session["user_lab_id"] = user.lab_id
            session["email"] = user.email
            return redirect(url_for('dashboard.dashboard_home'))

        flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)
