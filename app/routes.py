from app import app, db
from flask import render_template, flash, redirect, url_for, request
from app.forms import LoginForm, RegistrationForm, AccountForm, EditProfileForm, DepositForm, WithdrawForm, TransferForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Account
import sqlalchemy as sa
from urllib.parse import urlsplit
import random
from decimal import Decimal

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

@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    account =  db.first_or_404(sa.select(Account).where(Account.username==current_user.username))
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        account.mob_no = form.mob_no.data
        account.city = form.city.data
        account.pincode = form.pincode.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('user',username=current_user.username))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.mob_no.data = account.mob_no
        form.city.data = account.city
        form.pincode.data = account.pincode
    return render_template('edit_profile.html', title='Edit Profile', form=form)


@app.route('/deposit', methods=['GET', 'POST'])
@login_required
def deposit():
    form = DepositForm()
    account =  db.first_or_404(sa.select(Account).where(Account.username==current_user.username))

    if form.validate_on_submit():
        amount = form.amount.data
        past_amount = Decimal(account.balance)
        account.balance = str(amount+past_amount)
        db.session.commit()

        flash(f'Successfully deposited {amount} into your account!')
        return redirect(url_for('index'))

    return render_template('deposit.html', form=form, title='Deposit')

@app.route('/withdraw', methods=['GET', 'POST'])
@login_required
def withdraw():
    form = WithdrawForm()
    account =  db.first_or_404(sa.select(Account).where(Account.username==current_user.username))
    if form.validate_on_submit():
        amount = form.amount.data
        past_amount = Decimal(account.balance)
        # Check if the user has sufficient balance
        if past_amount >= amount:
            # Update the user's account balance
            account.balance = str(past_amount-amount)
            db.session.commit()

            flash(f'Successfully withdrew {amount} from your account!')
            return redirect(url_for('index'))
        else:
            flash('Insufficient funds')

    return render_template('withdraw.html', form=form, title='Withdraw')

@app.route('/transfer', methods=['GET', 'POST'])
@login_required
def transfer():
    form = TransferForm()

    if form.validate_on_submit():
        amount = form.amount.data
        receiver_username = form.receiver.data

        # Check if the receiver exists
        receiver = User.query.filter_by(username=receiver_username).first()
        if not receiver:
            flash('Receiver not found. Please check the username.')
            return redirect(url_for('transfer'))

        # Check if the sender has sufficient balance
        sender_account = Account.query.filter_by(username=current_user.username).first()
        sender_balance = Decimal(sender_account.balance)

        if sender_balance >= amount:
            # Update the sender's account balance
            sender_account.balance = str(sender_balance - amount)

            # Update the receiver's account balance
            receiver_account = Account.query.filter_by(username=receiver_username).first()
            receiver_balance = Decimal(receiver_account.balance)
            receiver_account.balance = str(receiver_balance + amount)

            db.session.commit()

            flash(f'Successfully transferred {amount} to {receiver_username}!')
            return redirect(url_for('index'))
        else:
            flash('Insufficient funds')

    return render_template('transfer.html', form=form, title='Transfer')
