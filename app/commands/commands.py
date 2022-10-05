import click
from flask.cli import with_appcontext
from werkzeug.security import generate_password_hash
from app.extensions import db
from app.auth.models import User, Role
from app.teaching.models import Subject


@click.command('init_db')
@with_appcontext
def init_db():
    db.drop_all()
    db.create_all()
    db.session.commit()
    click.echo("Created database")


@click.command('create_roles')
@with_appcontext
def create_roles():
    for role in ['admin','lecturer','intern','student']:
        new_role = Role(name=role)
        try:
            db.session.add(new_role)
            db.session.commit()
            click.echo(f'{role} role has been added!')
        except Exception as e:
            click.echo(e)


@click.command('add_subjects')
@with_appcontext
def add_subjects():
    subjects = [
        'Front - End', 'გრაფიკული დიზაინი', 'ICT პროექტების მართვა',
        'Python', 'ციფრული კომუნიკაციები', 'ნარატივ დიზაინი',
        'WordPress', 'PHP'
    ]
    for subject in subjects:
        s = Subject(
            name=subject,
        )
        try:
            db.session.add(s)
            db.session.commit()
            click.echo('Subjects has been added')
        except Exception as e:
            click.echo(e)