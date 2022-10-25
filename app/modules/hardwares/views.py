from flask import Blueprint, render_template, redirect, url_for, flash, request

from app.modules.hardwares.forms import HardwareForm
from app.modules.hardwares.models import Hardware
from app.modules.auth.models import User

hardware_blueprint = Blueprint('hardware', __name__, template_folder="templates")


@hardware_blueprint.route('/hardware', methods=['GET', 'POST'])
def hardware():
    form = HardwareForm()
    hardware_model = Hardware()

    if form.validate_on_submit():
        user_full_name = form.user_full_name.data
        user_name, user_last_name = user_full_name.split(' ')

        user = User.query.filter_by(name=user_name, last_name=user_last_name).first()

        if user:
            hardware_model.create(
                manufacturer=form.manufacturer.data,
                model=form.model.data,
                serial_number=form.serial_number.data,
                user_id=user.id
            )
            flash('Hardware added successfully', 'success')

        return redirect(url_for('hardware.hardware'))

    return render_template("hardware/hardware.html", form=form)
