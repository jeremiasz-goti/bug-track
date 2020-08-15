from flask import render_template, url_for, flash, redirect, request
from bugtrack.forms import RegistrationForm, LoginForm, IssueForm
from bugtrack.models import User, Issue
from bugtrack import app, db, bcrypt
from flask_login import login_user, logout_user, current_user, login_required



@app.route('/')
def welcome():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    else:
        return redirect(url_for('login'))

@app.route('/home')
def home():
    if current_user.is_authenticated:
        return render_template('home.html', title='Home')
    else:
        return redirect(url_for('login'))

@app.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    form = IssueForm()
    if form.validate_on_submit():
        issue = Issue(issue_title=form.issue_title.data, issue_type=form.issue_type.data, issue_content=form.issue_content.data, file=form.file.data)
        db.session.add(issue)
        db.session.commit()
        flash(f'Issue added.', 'succes')
        return redirect(url_for('home'))
    return render_template('add.html', title='Add Issue', form=form)

@app.route('/reports')
@login_required
def reports():
    return render_template('reports.html', title='My reports')

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


