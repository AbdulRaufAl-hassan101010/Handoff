from flask import render_template, url_for, flash, redirect, session, jsonify
from handoffmls import app, db
from handoffmls.forms import RegistrationForm, LoginForm, AddUserForm, CreateHandoffForm
from handoffmls.models import Lab, User, Handoff
from flask_bcrypt import Bcrypt
import json

from handoffmls.middlewares import authentication_required, is_logged_in

# init bcrypt
bcrypt = Bcrypt(app)


@app.route("/")
@app.route("/home")
@is_logged_in
def home():
    total_users = len(User.query.all())
    total_labs = len(Lab.query.all())
    return render_template("home.html", total_users=total_users, total_labs=total_labs)


@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/register", methods=['GET', 'POST'])
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
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
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
            return redirect(url_for('dashboard_home'))

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
            return redirect(url_for('dashboard_home'))

        flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)


def get_handoffs_data():
    user_id = session.get('user_id')
    lab_id = session.get('lab_id')
    user_email = session.get('email')
    handoffs_all = []
    handoffs_in_progress = []
    handoffs_completed = []
    query = []
    # if signed in as user display only handoffs user in involved in
    if user_id:
        query = Handoff.query.filter(Handoff.persons.like(f'%"{user_email}"%'))
        handoffs_all = query.all()
    else:
        # else if signed in as lab  desplay all  handoffs
        query = Handoff.query.filter_by(lab_id=lab_id)
        handoffs_all = query.all()

    # get handsoff base on status (in progress, completed)
    handoffs_in_progress = query.filter_by(
        status="in progress").all()
    handoffs_completed = query.filter_by(
        status="completed").all()

    return {'handoffs_all': handoffs_all, 'handoffs_in_progress': handoffs_in_progress, 'handoffs_completed': handoffs_completed}


@app.route("/dashboard")
@authentication_required
def render_home():
    data = get_handoffs_data()

    return render_template('dashboard/home.html', handoffs=data['handoffs_all'], handoffs_len=len(data['handoffs_all']), in_progess_len=len(data['handoffs_in_progress']), completed_len=len(data['handoffs_completed']), title="All Handoffs")


@app.route("/dashboard")
@app.route('/dashboard/<path>')
@authentication_required
def dashboard_home(path=None):
    data = get_handoffs_data()

    if path == "inprogress":
        return render_template('dashboard/home.html', handoffs=data['handoffs_in_progress'], handoffs_len=len(data['handoffs_all']), in_progess_len=len(data['handoffs_in_progress']), completed_len=len(data['handoffs_completed']),  title=path)
    elif path == "completed":
        return render_template('dashboard/home.html', handoffs=data['handoffs_completed'], handoffs_len=len(data['handoffs_all']), in_progess_len=len(data['handoffs_in_progress']), completed_len=len(data['handoffs_completed']),  title=path)

    return redirect(url_for('render_home'))


@app.route("/logout")
@authentication_required
def logout():
    session.clear()
    flash('You have been logged out', 'danger')
    return redirect(url_for('login'))


@app.route("/dashboard/users")
@authentication_required
def dashboard_users():
    # get username from session
    username = session.get('username')

    # get lab_id from session
    lab_id = session.get("lab_id")

    # get all users from database
    lab = Lab.query.get(lab_id)
    users = lab.employees
    return render_template('dashboard/users.html', username=username, page="dashboard", users=users, users_len=len(users))


@app.route("/dashboard/user/add", methods=['GET', 'POST'])
@authentication_required
def add_user():
    form = AddUserForm()
    if form.validate_on_submit():
        first_name = form.first_name.data
        last_name = form.last_name.data
        other_name = form.other_name.data
        email = form.email.data
        lab_id = session.get('lab_id')

        user = User(first_name=first_name, last_name=last_name,
                    email=email, other_name=other_name, lab_id=lab_id)
        db.session.add(user)
        db.session.commit()
        flash("User has been created!!!", "success")
        return redirect(url_for('add_user'))

    # get lab_id from session
    lab_id = session.get("lab_id")

    # get all users from database
    lab = Lab.query.get(lab_id)
    users = lab.employees
    return render_template('dashboard/add_user.html', title='Dashboard | Add user', form=form, users_len=len(users))


@app.route("/dashboard/create_handoff", methods=['GET', 'POST'])
@authentication_required
def create_handoff():

    # get user_id, lab_id sessions
    lab_id = session.get("user_lab_id")
    user_id = session.get("user_id")

    def get_users_in_lab():
        # get all users belonging to this lab from database
        lab = Lab.query.get(lab_id)
        users = lab.employees

        dynamic_values = [(f"{value.email}",
                           f"{value.first_name} {value.last_name}") for value in users]
        return dynamic_values

    form = CreateHandoffForm()
    # add users to wtf form modelto generate checkbox
    form.persons.choices = get_users_in_lab()

    if form.validate_on_submit():
        # added creator to person list
        user_email = session.get('email')
        form.persons.data.append(user_email)

        summary = form.summary.data
        persons = json.dumps(form.persons.data)
        actions = form.actions.data
        changes = form.changes.data
        evaluation = form.evaluation.data

        handoff = Handoff(summary=summary, persons=persons,
                          actions=actions, changes=changes, evaluation=evaluation, created_by=user_id, assign_to=user_id, lab_id=lab_id)
        db.session.add(handoff)
        db.session.commit()

        return redirect(url_for('dashboard_home'))

    return render_template("dashboard/create_handoff.html", form=form)


@app.route("/dashboard/profile")
@authentication_required
def profile():
    if session.get('user_id'):
        form = AddUserForm()
        form.submit.label.text = 'Update User'
    else:
        form = RegistrationForm()
        form.submit.label.text = 'Update Lab'
    return render_template("dashboard/profile.html", form=form)
