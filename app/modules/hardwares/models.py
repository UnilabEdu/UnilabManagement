from app.extensions import db
from app.database import BaseModel


class Hardware(db.Model, BaseModel):
    __tablename__ = 'hardware'

    id = db.Column(db.Integer, primary_key=True)
    manufacturer = db.Column(db.String(64), nullable=False, index=True)
    model = db.Column(db.String(64), nullable=False, index=True)
    serial_number = db.Column(db.String(64), nullable=False, index=True)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
