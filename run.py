from flask import Flask,render_template,redirect,request
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash,check_password_hash

app = Flask(__name__)
db = SQLAlchemy(app)#initialise connection
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:Access@localhost/users'


class registration(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(100))
    password = db.Column(db.String(300))

@app.route('/', methods=['POST','GET'])
def index():
    if request.method == 'POST':
        #get login details
        usernames = request.form['usernames']
        passwords = request.form['passwords']
        #get data from the database depending on the data provided
        get_userdet = registration.query.filter_by(username = usernames).first()
        result_password = get_userdet.password
        # result_password = get_userdet[0]
        #check if password matches
        varify_password = check_password_hash(result_password,passwords)
        if varify_password:
            return redirect('/home_page')
        else:
            return "Wrong password,please try again"
    title = "Login  with Flask"
    return render_template('index.html',title = title)

@app.route('/signup', methods=['POST','GET'])
def signups():
    # check if request methrod is POST
    if request.method == 'POST':
        #if the method is port the we get the details
        username = request.form['username']
        password = request.form['password']
        # hash the password with python built in function 
        # secure_password = generate_password_hash(password, method='pbkdf2:sha1', salt_length=8)
        secure_password = generate_password_hash(password)
        new_user = registration(username = username, password = secure_password)
        # check if no user has the following details
        # try:
        #         # add teh added details to the database
        #         db.session.add(new_user)
        #         db.session.commit()
        #         # if user details submited return a redirect to the login page
        #         return redirect('/')
        # except:
        #         # if not submited return an error
        #        return "Error submiting your details"
        get_details = registration.query.filter_by(username= username).first()
        if get_details:
            return "Username already taken"
        else:
            try:
                # add teh added details to the database
                db.session.add(new_user)
                db.session.commit()
                # if user details submited return a redirect to the login page
                return redirect('/')
            except:
                # if not submited return an error
               return "Error submiting your details"
    title = "Sign-Up with Flask"
    return render_template('signup.html', title = title)

@app.route('/home_page')
def home_page():
    return render_template('home.html')

if __name__ == '__main__':
    app.run(debug = True)