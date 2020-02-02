from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from __init__ import app, db
from models import user, goal, user_goal, success, comment, reaction
from models.mixin import timestamp_mixin

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
