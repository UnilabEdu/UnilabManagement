from flask import Blueprint, flash, url_for, \
    redirect, render_template, request, session
from flask_login import logout_user, login_required, current_user,login_user

from app.auth.forms import RegisterForm, LoginForm
from app.auth.models import User
from app.extensions import db,get_password,send_email_after_register

user_blueprint = Blueprint('user', __name__, template_folder="templates")

@user_blueprint.route('/')
def home():
    return render_template("base.html")


@user_blueprint.route('/registration', methods=['GET', 'POST'])
def registration():
    form = RegisterForm()

    if form.validate_on_submit():
            email = form.email.data
            # user = User.query.filter_by(email=email).first()
            # print('\n\n',user,'იუზერ\n\n')
            # if user:
            #     flash('email exists')
            print(request.form)
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
                role = form.status.data,
                password = get_password()
            )
            if user:
                # sent random password to user
                # send_email_after_register(user.email,user.password)
                pass
            db.session.add(user)
            db.session.commit()
            flash("რეგისტრაცია წარმატებით დასრულდა")

            return redirect(url_for('user.login'))
    if form.errors != {}: #If there are not errors from the validations
        for err_message in form.errors.values():
            flash(f'There was an error with creating a user: {err_message}', category='error')
    return render_template("registration.html", form = form)

@user_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
                user = User.find_by_email(form.email.data)
                session["logged_in"] = True


                if user is not None:
                    login_user(user)
                    flash("მომხმარებელმა წარმატებით გაიარა ავტორიზაცია")


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

