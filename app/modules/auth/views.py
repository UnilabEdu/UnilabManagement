import os

from flask import Blueprint, flash, url_for, redirect, render_template, request, session, request
from flask_login import logout_user, login_required, current_user, login_user
from werkzeug.security import generate_password_hash

from app.modules.auth.forms import RegisterForm, LoginForm, RequestResetForm, ResetPasswordForm
from app.extensions import db
from app.modules.auth.services import get_password, send_email
from app.modules.auth.models import User
from app.settings import PROJECT_ROOT


user_blueprint = Blueprint('user', __name__, template_folder="templates")


@user_blueprint.route('/')
def home():
    return render_template("base.html")


@user_blueprint.route('/registration', methods=['GET', 'POST'])
def registration():
    form = RegisterForm()

    if form.validate_on_submit():
        password = get_password()
        email = form.email.data
        user = User(
            name=form.first_name.data,
            last_name=form.last_name.data,
            email=email,
            gender=form.sex.data,
            birth_date=form.birth_date.data,
            phone_number=form.phone_number.data,
            passport_id=form.passport_id.data,
            country=form.country.data,
            city=form.city.data,
            region=form.region.data,
            address=form.address.data,
            # TODO: add role
            password=password
        )
        try:
            db.session.add(user)
            db.session.commit()
            flash("რეგისტრაცია წარმატებით დასრულდა")
            # create user directory in uploads/users
            os.mkdir(os.path.join(PROJECT_ROOT, f'uploads/users/{user.id}_{user.name}_{user.last_name}'))
            # sent random password to user
            try:
                send_email(
                    user = user,
                    subject=f'User Registration Successful!',
                    text=f'Hello {user.name}, You have successfuly registered.\
                    \nthis is your password: {password}'
                )
            except Exception as e:
                print(e)
            del password
            return redirect(url_for('user.login'))
        except Exception as e:
            print(e)

    if form.errors != {}:  # If there are not errors from the validations
        for err_message in form.errors.values():
            flash(f'There was an error with creating a user: {err_message}', category='error')

    return render_template("auth/registration.html", form=form)


@user_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.find_by_email(form.email.data)
        # session["logged_in"] = True
        if user:
            # login_user(user)
            if user.check_password(form.password.data):
                login_user(user, remember=form.remember.data)
                flash("Login Successfully", category="success")
                return redirect(url_for('user.welcome'))
            else:
                flash("Wrong Password - Try Again!", category="error")
        else:
            flash("User Doesn`t Exists! Try Again...", category='error')
            # next = request.args.get('next')
            #
            # if next is None:
            #     next = url_for('unilab.main')
            #
            # return redirect(next)

    return render_template("auth/login.html", form=form)


@user_blueprint.route('/welcome', methods=['GET', 'POST'])
@login_required
def welcome():
    return render_template("auth/welcome.html")



@user_blueprint.route('/logout', methods=['GET'])
def logout():
    logout_user()
    flash("მომხმარებელი გამოვიდა სისტემიდან")
    session["logged_in"] = False
    return render_template("base.html")


def send_reset_email(user):
    token = user.get_reset_token()
    send_email(
        user = user,
        subject = f'Password Reset Request',
        text =f'''To reset your password, visit the following link:\
            \n{url_for('user.reset_token', token=token, _external=True)}'''
    )


@user_blueprint.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return render_template('welcome.html')
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('user.login'))
    return render_template('auth/reset_request.html',  form=form)


@user_blueprint.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('user.welcome'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('user.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.password_hash = generate_password_hash(form.password.data)
        db.session.commit()
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('user.login'))
    return render_template('auth/reset_token.html',  form=form)
