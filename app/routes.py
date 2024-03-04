from app import app, db
from flask import render_template, flash, redirect, url_for, request
from app.forms import LoginForm, RegistrationForm, AccountForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Account
import sqlalchemy as sa
from urllib.parse import urlsplit
import random

@app.route('/')
@app.route('/index')
@login_required
def index():
    return render_template('index.html',title='Home')


@app.route('/login', methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(sa.select(User).where(User.username==form.username.data))
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        
        login_user(user, remember=form.remember_me.data)

        next_page = request.args.get('next')
        if not next_page or urlsplit(next_page).netloc != '':
            next_page = url_for('index')

        return redirect(next_page)

    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = RegistrationForm()
    
    if form.validate_on_submit():
        # Create a new user
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        
        db.session.add(user)
        db.session.commit()
        
        flash('Congratulations, you are now a registered user!')
        
        # Redirect to the account creation page with the new user's information
        return redirect(url_for('account_creation', username=form.username.data))

    return render_template('register.html', title='Register', form=form)

@app.route('/account_creation', methods=['GET', 'POST'])
def account_creation():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = AccountForm()

    if form.validate_on_submit():
        # Retrieve the username from the URL parameters
        username = request.args.get('username')

        # Check if the username is provided
        if username:
            balance = 0
            account_no = '{:012}'.format(random.randint(0, 10**12 - 1))
            
            # Create an account linked to the registered user
            account = Account(
                account_no=account_no,
                balance=balance,
                mob_no=form.mob_no.data,
                city=form.city.data,
                pincode=form.pincode.data,
                pancard_no=form.pancard_no.data,
                account_type=form.account_type.data,
                username=username  # Use the provided username
            )

            db.session.add(account)
            db.session.commit()

            flash('Your account is successfully created')
            return redirect(url_for('login'))

    return render_template('account_creation.html', form=form, title="Account Creation")

@app.route('/user/<username>')
@login_required
def user(username):
    user = db.first_or_404(sa.select(User).where(User.username==username))
    account = db.first_or_404(sa.select(Account).where(Account.username==username))
    return render_template('user.html', user=user,account=account)



