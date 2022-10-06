from flask import Blueprint, flash, url_for, \
    redirect, render_template, request, session, request
from flask_login import logout_user, login_required, current_user, login_user
from app.auth.forms import RegisterForm, LoginForm
from app.extensions import db, get_password, send_email_after_register 
from app.auth.models import User
from app.configs import PROJECT_ROOT
import os


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
            name = form.first_name.data,
            last_name = form.last_name.data,
            email = email,
            gender = form.sex.data,
            birth_date = form.birth_date.data,
            phone_number = form.phone_number.data,
            passport_id = form.passport_id.data,
            country = form.country.data,
            city = form.city.data,
            region = form.region.data,
            address = form.address.data,
            # TODO add role
            password = password
        )
        try:
            db.session.add(user)
            db.session.commit()
            flash("რეგისტრაცია წარმატებით დასრულდა")
            # create user directory in uploads/users
            os.mkdir(os.path.join(PROJECT_ROOT, f'static/uploads/users/{user.id}_{user.name}_{user.last_name}'))
            # sent random password to user
            send_email_after_register(user,password)
            del password
            return redirect(url_for('user.login'))
        except Exception as e:
                print(e)
    if form.errors != {}: #If there are not errors from the validations
        for err_message in form.errors.values():
            flash(f'There was an error with creating a user: {err_message}', category='error')
    return render_template("registration.html", form = form)

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

    return render_template("login.html", form = form)




@user_blueprint.route('/welcome', methods=['GET', 'POST'])
@login_required
def welcome():

    return render_template("welcome.html")

# @user_blueprint.route('/logout', methods=['GET'])
# def logout():
#     logout_user()
#     flash("მომხმარებელი გამოვიდა სისტემიდან")
#     session["logged_in"] = False
#     return render_template("base.html")
#

@user_blueprint.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    pass