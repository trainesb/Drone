import click
from app import create_app, db
from app.models.Controller import Controller
from app.models.PID import PID

app = create_app()

@app.cli.command('db_init')
def db_init():
    Controller.query.delete()
    PID.query.delete()
    pid = PID()
    controller = Controller()
    db.session.add(pid)
    db.session.add(controller)
    db.session.commit()
