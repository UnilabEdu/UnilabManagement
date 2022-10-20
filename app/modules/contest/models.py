from app.extensions import db
from app.database import BaseModel


class ListOfContest(db.Model, BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    type_of_contest = db.Column(db.String(64), nullable=False, index=True)
    name_of_contest = db.Column(db.String(64), nullable=False, index=True)
    status = db.Column(db.String(64), nullable=False, unique=True, index=True)
    start_date = db.Column(db.Date())
    end_date = db.Column(db.Date(), nullable=False)
    number_of_participants = db.Column(db.Integer, nullable=False)


class ListOfTests(db.Model, BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    direction = db.Column(db.String(64), nullable=False, index=True)
    test_title = db.Column(db.String(64), nullable=False, index=True)
    describe = db.Column(db.String(), nullable=False, unique=True, index=True)
    type = db.Column(db.String(225))
    status = db.Column(db.String(64), nullable=False)
    compiler = db.Column(db.Integer, nullable=False)
