from pyexpat import model
from app.extensions import db
from app.database import BaseModel


class Hardware(db.Model, BaseModel):
    id = db.Column(db.Integer, primary_key=True)

    # devices_type = db.Column(db.String(64), db.ForeignKey("devices_type.id"))
    # name = db.Column(db.String(64), nullable=False, index=True)
    # qr_code = db.Column(db.String(), nullable=False, unique=True, index=True)
    # status = db.Column(db.String(225), default="active")
    # date_of_creation = db.Column(db.Date())
    # note = db.Column(db.String(225))

    manufacturer = db.Column(db.String(64), nullable=False, index=True)
    model = db.Column(db.String(64), nullable=False, index=True)
    serial_number = db.Column(db.String(64), nullable=False, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
