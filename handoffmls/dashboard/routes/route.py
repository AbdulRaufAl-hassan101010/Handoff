from flask import render_template, url_for, flash, redirect, session, request
from handoffmls import app, db
from handoffmls.dashboard import dashboard
from handoffmls.forms import RegistrationForm
from handoffmls.dashboard.forms import AddUserForm, CreateHandoffForm
from handoffmls.models import Lab, User, Handoff, Task
from flask_bcrypt import Bcrypt
import json

from handoffmls.middlewares import authentication_required

# init bcrypt
bcrypt = Bcrypt(app)


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


@dashboard.route("/")
@authentication_required
def render_home():
    data = get_handoffs_data()

    return render_template('dashboard/home.html', handoffs=data['handoffs_all'], handoffs_len=len(data['handoffs_all']), in_progess_len=len(data['handoffs_in_progress']), completed_len=len(data['handoffs_completed']), title="All Handoffs")


@dashboard.route("/")
@dashboard.route('/<path>')
@authentication_required
def dashboard_home(path=None):
    data = get_handoffs_data()

    if path == "inprogress":
        return render_template('dashboard/home.html', handoffs=data['handoffs_in_progress'], handoffs_len=len(data['handoffs_all']), in_progess_len=len(data['handoffs_in_progress']), completed_len=len(data['handoffs_completed']),  title=path)
    elif path == "completed":
        return render_template('dashboard/home.html', handoffs=data['handoffs_completed'], handoffs_len=len(data['handoffs_all']), in_progess_len=len(data['handoffs_in_progress']), completed_len=len(data['handoffs_completed']),  title=path)

    return redirect(url_for('dashboard.render_home'))


@dashboard.route("/logout")
@authentication_required
def logout():
    session.clear()
    flash('You have been logged out', 'danger')
    return redirect(url_for('landingpage.login'))


@dashboard.route("/users")
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


@dashboard.route("/user/add", methods=['GET', 'POST'])
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
        return redirect(url_for('dashboard.add_user'))

    # get lab_id from session
    lab_id = session.get("lab_id")

    # get all users from database
    lab = Lab.query.get(lab_id)
    users = lab.employees
    return render_template('dashboard/add_user.html', title='Dashboard | Add user', form=form, users_len=len(users))


@dashboard.route("/create_handoff", methods=['GET', 'POST'])
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
    # add susers to wtf form modelto generate checkbox
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

        # if error with adding task delete handoff
        if 'count' not in request.form:
            # remove handoff
            db.session.delete(handoff)
            db.session.commit()

        tasks = []
        task_count = int(request.form['count'])
        try:
            for i in range(1, task_count + 1):
                task_description = request.form.get(f'task-{i}')

                # Convert checkbox value to boolean
                task_status = bool(request.form.get(f'task-status-{i}'))

                task = Task(description=task_description,
                            completed=task_status)
                tasks.append(task)

            # Associate tasks with the handoff
            handoff.tasks = tasks

            db.session.commit()
        # Code to execute after successful commit
        except Exception as e:
            db.session.rollback()
            # Code to handle the error
            print(e)

        # redirect
        return redirect(url_for("dashboard.dashboard_home"))
    return render_template("dashboard/create_handoff.html", form=form)


@dashboard.route("/profile",  methods=["GET"])
@authentication_required
def profile():
    user_id = session.get('user_id')

    if user_id:
        form = AddUserForm()
        form.submit.label.text = 'Update User'

        data = User.query.get(user_id)

        if data:
            form.first_name.data = data.first_name
            form.last_name.data = data.last_name
            form.other_name.data = data.other_name
            form.email.data = data.email

    else:
        form = RegistrationForm()
        form.submit.label.text = 'Update Lab'
        data = {}
    return render_template("dashboard/profile.html", form=form)


@dashboard.route("/profile", methods=["POST"])
@authentication_required
def update_user():
    user_id = session.get('user_id')
    form = AddUserForm()
    data = User.query.get(user_id)
    print(form.email.data)
    if form.validate_on_submit():
        data.first_name = form.first_name.data
        data.last_name = form.last_name.data
        data.other_name = form.other_name.data
        data.email = form.email.data
        db.session.commit()

    return redirect(url_for('dashboard.profile'))


@dashboard.route("/tasks")
@dashboard.route("/tasks/<id>")
def tasks_html(id=None):
    handoff = Handoff.query.get(id)
    tasks = handoff.tasks
    all_completed = all(task.completed for task in tasks)
    if all_completed and handoff.status == "in progress":
        handoff.status = "completed"
        db.session.commit()
    return render_template("dashboard/tasks.html", tasks=tasks, enumerate=enumerate, all_completed=all_completed)


@dashboard.route("/tasks/<id>", methods=["POST"])
def tasks_post(id):
    handoff = Handoff.query.get(id)
    tasks = handoff.tasks
    try:

        for task in tasks:
            index = tasks.index(task)
            if task.completed == False:
                task.completed = bool(request.form.get(str(index)))
        all_completed = all(task.completed for task in tasks)
        if all_completed:
            handoff.status = "completed"
        print(handoff.status)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(e)

    return render_template("dashboard/tasks.html", tasks=tasks, enumerate=enumerate, all_completed=all_completed)
