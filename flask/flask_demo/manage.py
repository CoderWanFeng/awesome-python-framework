from flask_script import Manager

from apps import init_app

app = init_app()
manage = Manager(app)

if __name__ == '__main__':
    manage.run()
