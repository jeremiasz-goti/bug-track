from flask import render_template, url_for, flash, redirect
from bugtrack.forms import RegistrationForm, LoginForm, IssueForm
from bugtrack.models import User, Issue
from bugtrack import app, db, bcrypt



@app.route('/')
def home():
    return render_template('home.html')

@app.route('/add', methods=['GET', 'POST'])
def add():
    form = IssueForm()
    if form.validate_on_submit():
        return redirect(url_for('home'))
    return render_template('add.html', title='Add Issue', form=form)

@app.route('/reports')
def reports():
    return render_template('reports.html', title='My reports')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User(email=form.email.data, password=form.password.data)
        flash(f'User logged in.', 'success')
        return redirect(url_for('home'))
    else:
        flash(f'Error - check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)
