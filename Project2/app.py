from flask import Flask,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, migrate

app = Flask(__name__)
app.debug = True

#db_name='site.db'

# adding configuration for using a sqlite database
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://ditiss:iacsd123@192.168.80.148/flaskapp"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Creating an SQLAlchemy instance
db = SQLAlchemy(app)
# Settings for migrations
migrate = Migrate(app, db)

# Models
class Profile(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	first_name = db.Column(db.String(20), unique=False, nullable=False)
	last_name = db.Column(db.String(20), unique=False, nullable=False)
	username = db.Column(db.String(100),unique=False, nullable=False)
	email = db.Column(db.String(200), unique=False, nullable=False)
	password = db.Column(db.String(100), unique=True)
	age = db.Column(db.Integer, nullable=False)

	def __repr__(self):
	       	return f"Name : {self.first_name}, Age: {self.age}"

# function to render index page
@app.route('/')
def index():
        #profiles = Profile.query.all()
        return render_template('index.html')


@app.route('/login', methods=["POST"])
def user_login():
	email_id = request.form.get("username")
	pw = request.form.get("password")
	print("Email: ", email_id)
	print("pw: ", pw)
	if email_id and pw:
		user = Profile.query.filter_by(email=email_id).first()
		print("Login User: ",user)
		if user:
			profiles = Profile.query.all()
			return render_template('view_users.html',profiles=profiles)
		else:
			return render_template('index.html')
	else:
		return render_template('index.html')
# function to render index page
@app.route('/view_users')
def viewusers():
        profiles = Profile.query.all()
        return render_template('view_users.html',profiles=profiles)


@app.route('/add_data')
def add_data():
        return render_template('add_profile.html')


# function to add profiles
@app.route('/add', methods=["POST"])
def profile():

	# In this function we will input data from the
	# form page and store it in our database.
	# Remember that inside the get the name should
	# exactly be the same as that in the html
	# input fields
	fn = request.form.get("first_name")
	ln = request.form.get("last_name")
	email_id = request.form.get("email")
	Age = request.form.get("age")
	Password = request.form.get("password")
	#print("first name: ", first_name)
	#print("last name: ", last_name)
	#print("email: ", email)
	#print("age: ", age)
	# create an object of the Profile class of models
	# and store data as a row in our datatable
	if fn != '' and ln != '' and email_id!='' and Password!=''  and Age is not None:
		p = Profile(first_name=fn, last_name=ln,password=Password,age=Age,username=fn,email=email_id)
		db.session.add(p)
		db.session.commit()
		return redirect('/view_users')
	else:
		return redirect('/view_users')

@app.route('/delete/<int:id>')
def erase(id):
    # deletes the data on the basis of unique id and
    # directs to home page
	data = Profile.query.get(id)
	db.session.delete(data)
	db.session.commit()
	return redirect('/view_users')


if __name__ == '__main__':
        app.run(host='0.0.0.0', port=5000)


