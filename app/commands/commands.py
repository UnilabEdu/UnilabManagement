import click
from flask.cli import with_appcontext
from app.extensions import db
from app.auth.models import User, Role
from werkzeug.security import generate_password_hash


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


@click.command('init_db')
@with_appcontext
def init_db():
    db.drop_all()
    db.create_all()
    db.session.commit()
    click.echo("Created database")
