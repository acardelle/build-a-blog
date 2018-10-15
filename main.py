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
   title = db.Column(db.String(120))
   body_text = db.Column(db.String(240))
   owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
   completed = db.Column(db.Boolean)   

   def __init__(self, title, body_text, owner):
       self.title = title
       self.body_text = body_text
       self.owner = owner
       self.completed = False
      

class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    postings = db.relationship('Blog', backref='owner')

    def __init__(self, email, password):
        self.email = email
        self.password = password

@app.before_request
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
    return redirect('/')

@app.route('/', methods=['POST','GET'])
def index():

    postings = Blog.query.filter_by(completed = False).all()
    completed_postings = Blog.query.filter_by(completed = True).all()

    return render_template('blog.html', title="Get It Bloged!", postings=postings, completed_postings=completed_postings)

@app.route('/newpost', methods=['POST','GET'])
def newpost():

    owner = User.query.filter_by(email=session['email']).first()

    if request.method == 'POST':
        posting_title = request.form['posting_title']
        posting_text = request.form['posting_text']
        if (posting_title == '' == False) or (posting_text == '' == False):
            new_posting = Blog(posting_title, posting_text, owner)
            db.session.add(new_posting)
            db.session.commit()
            return redirect('/')
        else:
            post_error = 'Please provide a blog post title and post body.'
            return render_template('newpost.html',post_error=post_error)
    else:
        return render_template('newpost.html')


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