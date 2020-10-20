import click
from app import create_app, db
from app.models.Controller import Controller

app = create_app()

@app.cli.command('db_init')
def db_init():
    controller = Controller()
    db.session.add(controller)
    db.session.commit()
