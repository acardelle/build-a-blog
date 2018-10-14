from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:cake@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'y337'

class Blog(db.Model):

   id = db.Column(db.Integer, primary_key=True)
   name = db.Column(db.String(120))
   completed = db.Column(db.Boolean)
   owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))   

   def __init__(self, name):
       self.name = name
       self.completed = False

class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    postings = db.relationship('Blog', backref='owner')

    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.owner = owner

"""@app.before_request
def require_login():
    allowed_routes = ['login', 'register']
    if request.endpoint not in allowed_routes and 'email' not in session:
        return redirect('/login')

 
@app.route('/login', methods=['POST', 'GET'])
def login():

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and user.password == password:
            session['email'] = email
            flash("Logged in")
            return redirect('/')
        else:
            flash('User password incorrect, or user does not exist', 'error')

    return render_template('login.html')

@app.route('/register', methods=['POST', 'GET'])
def register():

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        verify = request.form['verify']

        # TODO - validate user's data

        existing_user = User.query.filter_by(email=email).first()
        if not existing_user:
            new_user = User(email, password)
            db.session.add(new_user)
            db.session.commit()
            session['email'] = email
            return redirect('/')
        else:
            # TODO - user better response messaging
            return "<h1>Duplicate user</h1>"


    return render_template('register.html')

@app.route('/logout')
def logout():
    del session['email']
    return redirect('/')"""

@app.route('/', methods=['POST','GET'])
def index():


    owner = User.query.filter_by(email=session['email']).first()

    if request.method == 'POST':
        posting_name = request.form['posting']
        new_posting = Blog(posting_name, owner)
        db.session.add(new_posting)
        db.session.commit()
    
        postings = Blog.query.filter_by(completed = False, owner=owner).all()
        completed_postings = Blog.query.filter_by(completed = True).all()

        return render_template('todos.html', title="Get It Bloged!", postings=postings, 
            completed_postings=completed_postings)

"""@app.route('/delete-task', methods=['POST'])
def delete_task():

    task_id = int(request.form['task-id'])
    task = Task.query.get(task_id)
    task.completed = True
    db.session.add(task)
    db.session.commit()

    return redirect("/")"""

if __name__ == '__main__':
    app.run()