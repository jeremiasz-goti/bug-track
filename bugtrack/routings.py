import os
import secrets
from flask import render_template, url_for, flash, redirect, request
from bugtrack.forms import RegistrationForm, LoginForm, IssueForm
from bugtrack.models import User, Issue
from bugtrack import app, db, bcrypt
from flask_login import login_user, logout_user, current_user, login_required
from sqlalchemy import desc

"""

File for handling application routes.

Define basic route by

@app.route('/endpoint')
def endpoint():
    define forms and logic for endpoint

    return render_template ('endpoint.html', title='endpoint', data=data)

Use @login_required for handling user sessions and restrictions.

"""

@app.route('/')
def welcome():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    else:
        return redirect(url_for('login'))

@app.route('/home', methods=['GET'])
def home():
    if current_user.is_authenticated:
        issues = db.session.query(Issue).order_by(desc('id'))
        return render_template('home.html', title='Home', issues=issues)
    else:
        return redirect(url_for('login'))

def save_file(form_file):
    file_hex = secrets.token_hex(8)
    f_name, f_ext = os.path.splitext(form_file.filename)
    file_name = file_hex + f_ext
    file_path = os.path.join(app.root_path, 'static/files', file_name)
    form_file.save(file_path)
    return file_name


@app.route('/issue/add', methods=['GET', 'POST'])
@login_required
def add():
    form = IssueForm()
    form_file = None
    if form.validate_on_submit():
        if form.file.data:
            form_file = save_file(form.file.data)
        issue = Issue(issue_title=form.issue_title.data, issue_content=form.issue_content.data, file=form_file, author=current_user)
        db.session.add(issue)
        db.session.commit()
        flash(f'Issue added.', 'success')
        return redirect(url_for('home'))
    return render_template('add.html', title='Add Issue', form=form)

@app.route('/reports', methods=['GET'])
@login_required
def reports():
    issues = db.session.query(Issue).order_by(desc('id'))

    return render_template('reports.html', title='My reports', issues=issues)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember_user.data)
            send_to = request.args.get('next')
            return redirect(send_to) if send_to else redirect(url_for('home'))
        else:
            flash(f'Error - check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/settings')
@login_required
def settings():
    return render_template('settings.html', title='Settings')


