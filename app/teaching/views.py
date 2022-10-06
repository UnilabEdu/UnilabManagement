from flask import Blueprint, flash, url_for, \
    redirect, render_template, request, session, request
from flask_login import logout_user, login_required, current_user, login_user
from werkzeug.utils import secure_filename
from app.extensions import db, get_password, send_email_after_register 
from app.teaching.models import Courses, Subject, UserCourses
from app.teaching.forms import CoursesForm, SubjectForm
from app.configs import PROJECT_ROOT
import os


teaching_blueprint = Blueprint('teaching', __name__, template_folder="templates")


@teaching_blueprint.route('/add/subject', methods=['GET', 'POST'])
def add_subject():
    form = SubjectForm()

    if form.validate_on_submit():
        name = form.name.data
        has_intership = form.has_intership.data
        s = Subject.query.filter_by(name=name).first()
        if s:
            flash('Subject already exists!', category='error')

        # create directory for that subject
        os.mkdir(os.path.join(PROJECT_ROOT, f'static/uploads/subjects/{name}'))
        try:
            sylabus = form.sylabus.data.filename
        except Exception as e:
            print(e)
            sylabus = None

        if sylabus:
            sylabus_name = secure_filename(form.sylabus.data.filename)

            # save sylabus in subject`s directory
            form.sylabus.data.save(f'{PROJECT_ROOT}/static/uploads/subjects/{name}/{sylabus_name}')
            # asign var sylabus address to save in db
            sylabus = f'{PROJECT_ROOT}/static/uploads/subjects/{name}/{sylabus_name}'

        else:
            sylabus = None
        # add new subject to db
        new_subject = Subject(
            name=name,
            has_intership=has_intership,
            sylabus=sylabus
        )
        try:
            db.session.add(new_subject)
            db.session.commit()
            flash(f'{new_subject.name} has been added in subjects.', category='success')
        except Exception as e:
            print(e)
            flash(e, category='error')
    return render_template('add_subject.html', form=form)


