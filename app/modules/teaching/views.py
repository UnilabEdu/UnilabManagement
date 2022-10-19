import os

from flask import Blueprint, flash, render_template, request, url_for
from werkzeug.utils import secure_filename

from app.extensions import db
from app.settings import PROJECT_ROOT
from app.modules.teaching.models import Courses, Subject, UserCourses
from app.modules.teaching.forms import CoursesForm, SubjectForm


teaching_blueprint = Blueprint('teaching', __name__, template_folder="templates")


@teaching_blueprint.route('/add/subject', methods=['GET', 'POST'])
def add_subject():
    form = SubjectForm()

    if form.validate_on_submit():
        name = form.name.data
        has_internship = form.has_internship.data
        s = Subject.query.filter_by(name=name).first()
        if s:
            flash('Subject already exists!', category='error')

        # create directory for that subject
        os.mkdir(os.path.join(PROJECT_ROOT, f'static/uploads/subjects/{name}'))
        try:
            syllabus = form.syllabus.data.filename
        except Exception as e:
            print(e)
            syllabus = None

        if syllabus:
            syllabus_name = secure_filename(form.syllabus.data.filename)

            # save syllabus in subject`s directory
            form.syllabus.data.save(f'{PROJECT_ROOT}/static/uploads/subjects/{name}/{syllabus_name}')
            # assign var syllabus address to save in db
            syllabus = f'{PROJECT_ROOT}/static/uploads/subjects/{name}/{syllabus_name}'

        else:
            syllabus = None
        # add new subject to db
        new_subject = Subject(
            name=name,
            has_internship=has_internship,
            syllabus=syllabus
        )
        try:
            db.session.add(new_subject)
            db.session.commit()
            flash(f'{new_subject.name} has been added in subjects.', category='success')
        except Exception as e:
            print(e)
            flash("Error while saving to the database.", category='error')
    return render_template('teaching/add_subject.html', form=form)


