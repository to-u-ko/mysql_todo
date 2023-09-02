from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

app = Flask(__name__)

app.config['SECRET_KEY]'] = 'mysite'
database_info = {
    'rdb': 'mysql',
    'user': "todo_user",
    'password': "todoApp",
    'host': "localhost",
    'db_name': "todo_DB"
    }
app.config['SQLALCHEMY_DATABASE_URI'] = '{rdb}://{user}:{password}@{host}/{db_name}?charset=utf8'.format(**database_info)

app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False

db.init_app(app)
migrate.init_app(app, db)

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True)

    def __init__(self, username):
        self.username = username

@app.route('/', methods=['GET', 'POST'])
def write_db():
    if request.method == 'POST':
        username = request.form.get('username')
        user = User(username=username)
        try:
            with db.session.begin(subtransactions=True):
                db.session.add(user)
            db.session.commit()
        except:
            db.session.rollback()
            raise
        finally:
            db.session.close()

        return redirect(url_for('read_db'))
    return render_template('insert.html')

@app.route('/read_db')
def read_db():
    users = db.session.query(User).order_by(User.id.desc()).first()
    return render_template('user.html', users=users)

if __name__=='__main__':
    app.run(debug=True, host='0.0.0.0')