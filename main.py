from flask import Flask, render_template,  request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ums.sqlite'
app.config['SECRET_KEY'] = "11ac4aed80a031a0d2c71db4"
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(255), nullable=False)
    lname = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    username = db.Column(db.String(255), nullable=False)
    edu = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    status = db.Column(db.Integer,default= 0, nullable=False)

    def __ref__(self):
        return f'User("{self.lname}","{self.fname}","{self.email}","{self.username}","{self.edu}","{self.password}","{self.status}","{self.id}")'

    # def __init__(self, name, email, password, role):
    #     self.name = name
    #     self.email = email
    #     self.password = password
    #     self.role = role


    def __repr__(self):
        return '<User %r>' % self.name

# create table
with app.app_context():
    db.create_all()

# main index
@app.route('/')
def index():
    return render_template('index.html', title='Home')

@app.route('/admin/')
def adminIndex():
    return render_template('admin/index.html', title='Admin Login')

@app.route('/user/')
def userIndex():
    return render_template('user/index.html', title='User Login')

# User Register
@app.route('/user/signup/', methods=['POST', 'GET'])
def userSignup():
    if request.method == 'POST':
        fname = request.form['fname']
        lname = request.form['lname']
        email = request.form['email']
        username = request.form['username']
        edu = request.form['edu']
        password = request.form['password']
        # Verify if all the fields are filled or not
        if fname == "" or lname == "" or email == "" or username == "" or edu == "" or password == "":
            flash("Please fill all the fields", "danger")
        else:
            is_email = User.query.filter_by(email=email).first()
            if is_email:
                flash("Email already exists", "danger")
                return redirect('/user/signup/')
            else:
                hash_password = bcrypt.generate_password_hash(password, 10).decode('utf-8')
                user = User(fname=fname, lname=lname, email=email, username=username, edu=edu, password=hash_password)
                db.session.add(user)
                db.session.commit()
                flash("Account created successfully, Admin will approve your account!", "success")
                return redirect('/user/')
    else:
        return render_template('user/signup.html', title='User Signup')

if __name__ == '__main__':
    app.run(debug=True)