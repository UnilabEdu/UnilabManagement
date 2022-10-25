from app.extensions import db
from app.database import BaseModel


class Device(db.Model, BaseModel):
    id = db.Column(db.Integer, primary_key=True)

    devices_type = db.Column(db.String(64), db.ForeignKey("devices_type.id"))

    name = db.Column(db.String(64), nullable=False, index=True)
    qr_code = db.Column(db.String(), nullable=False, unique=True, index=True)
    status = db.Column(db.String(225), default="active")
    date_of_creation = db.Column(db.Date())
    note = db.Column(db.String(225))


class DevicesType(db.Model, BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    devices_type = db.Column(db.String())
    type = db.relationship(Device, backref='worker', lazy="dynamic")
