from app.extensions import db


class BaseModel:
    """
    This Class describe SQLAlchemy DB model with Basic CRUD functionality

    atribs:
        - id: primery key
        - create
        - update
        - delete
        - save
        - read
    """

    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)

    @classmethod
    def load_all(cls):
        cls.query.all()

    def create(self, commit=True, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

        if commit:
            self.save()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def delete(self):
        db.session.delete(self)
        db.session.commit()
