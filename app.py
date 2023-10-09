from flask import Flask, render_template, redirect, url_for, request, session, flash

from flask_sqlalchemy import SQLAlchemy

#Creating an instance and storing it in the app object.
app = Flask(__name__)

#Creating the database and locating the database which will be used.
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///donation_data.db'
#Secret key is used for sessions.
app.secret_key = 'donate_data'
#Creating an instance of database.
db = SQLAlchemy(app)


#Creaing table for Registration form
class RegisterForm (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(80), nullable=False)

#Submit button functionality in register.html
@app.route('/register_form_submit', methods=['GET','POST'])
def register_form_submit():
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    phone = request.form['phone']
    address = request.form['address']

    # Query all details
    details = RegisterForm.query.all()
    print(details)
    # try to iterate
    for row in details:
        print(row.username, row.email, row.password, row.phone, row.address)

    register_form = RegisterForm(username=username, email=email, password=password, phone=phone, address=address)
    db.session.add(register_form)
    db.session.commit()

    message = 'Your details have been submitted'
    return render_template('login.html', message=message)


#Login Functionality
# Check if the user is authenticated and redirect to index.html
@app.route('/submit_form', methods=['POST'])
def submit_form():
    username = request.form['username']
    password = request.form['password']

    # Query all users
    users = RegisterForm.query.all()
    print(users)
    # try to iterate
    for row in users:
        print(row.username, row.password)
    # Query the database for a user with the given username and password
    user = RegisterForm.query.filter_by(username=username, password=password).first()

    # If the user is authenticated, redirect to index.html
    if user is not None:
        return redirect(url_for('index'))

    # If the user is not authenticated, store an error message and redirect to login.html
    flash('Invalid username or password')
    return redirect(url_for('login'))


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/services')
def services():
    return render_template("services.html")


@app.route('/register',methods=['POST','GET'])
def register():
    return render_template("register.html")


@app.route('/aboutus')
def aboutus():
    return render_template("aboutus.html")


@app.route('/login')
def login():
    return render_template("login.html")

@app.route('/dashboard')
def dashboard():
    return render_template("dashboard.html")

@app.route('/analytics')
def analytics():
    return render_template("analytics.html")


if __name__ == "__main__":
    with app.app_context():
        db.create_all()

        db.session.commit()
    app.run(debug=True)
