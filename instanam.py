import psycopg2
from flask import Flask, make_response, render_template, request, redirect,session,url_for
import bcrypt
import cloudinary
import cloudinary.uploader
import os
CLOUDINARY_CLOUD = os.environ.get('CLOUDINARY_CLOUD')
CLOUDINARY_API_KEY = os.environ.get('CLOUDINARY_API_KEY')
CLOUDINARY_API_SECRET = os.environ.get('CLOUDINARY_API_SECRET')

cloudinary.config(
    cloud_name = CLOUDINARY_CLOUD,
    api_key = CLOUDINARY_API_KEY,
    api_secret = CLOUDINARY_API_SECRET,
)
# from models.db import sql_select

app = Flask(__name__)

app.config['SECRET_KEY'] = 'This is a pretend secret key'

@app.route("/")
def index():

    return render_template('loginpage.html')

#HOME PAGE
@app.route("/homepage", methods=['GET'])
def homepage():
    # if session['name'] == True:
    name = session['name'] 
    username = session['username']

    return render_template("homepage.html",name=name,username=username)


#LOGIN/LOGOUT
@app.route("/loginpageaction", methods=['POST'])
def loginpageaction():
    conn = psycopg2.connect("dbname=instanam")
    cur = conn.cursor()
    
    username = request.form['username']    
    password = request.form['password']
    print(password)


    hashed_password = cur.execute(f'SELECT password_hash FROM users WHERE username = %s', [username])
    hashed_password, = cur.fetchone()
    print(password)
    valid = bcrypt.checkpw(password.encode(), hashed_password.encode())
    
    if valid:
        print("match")
        # session.pop('incorrect', default=None)
        cur.execute(f'SELECT name,username FROM users WHERE username = %s', [username])
        user_reccord = cur.fetchone()
        name,username = user_reccord
       
        session['name'] = name
        session['username'] = username
        cur.close()
        conn.close()
        return redirect("/homepage")
    else:
        print("wrong password")
        session['incorrect'] = "Incorrect Username or Password"
        
        return redirect('/')

    # cur.execute(f'SELECT id,name, FROM users WHERE username = %s AND password = %s', [username,password])

    # user_record = cur.fetchone()
    # user_id, sql_select_email = user_record

    # cur.close()
    # conn.close()
    
    # return redirect("/homepage")

@app.route("/logoutpageaction")
def logoutpageaction():
    response = redirect('/')
    session.clear()
    return response






#SIGN UP PAGE
@app.route("/signuppage")   
def signuppage():
    
    return render_template("signuppage.html")

@app.route("/signuppageaction", methods=['POST'])   
def signuppagaction():
    conn = psycopg2.connect("dbname=instanam")
    cur = conn.cursor()
    name = request.form.get('name')
    username = request.form.get('username')
    password = request.form.get('password')
    password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode('utf-8')
    cur.execute('INSERT INTO users (name,username,password_hash) VALUES (%s, %s, %s) RETURNING id ', [name,username,password_hash])
    details, = cur.fetchone()
    session['name'] = name
    session['username'] = username
    
    

    conn.commit()
    cur.close() 
    conn.close()
    return redirect("/homepage")




#USER DISPLAY PAGE
@app.route("/displayuserspage",methods=['POST'])
def displayuserspage():
    return render_template("displayuserspage.html")




#POST IMAGE PAGE
@app.route("/postimagepage",methods=['POST'])
def postimagepage():
    return render_template("postimagepage.html")

@app.route("/postimagepageaction", methods=['POST'])
def postimagepageaction():
    image = request.files['image']

    response = cloudinary.uploader.upload(image, filename=image.filename)
    
    
    image_id = response['public_id']

    return redirect(url_for('modified', id=image_id))



@app.route("/modified/<id>",methods=['POST'])
def modified(id):
    cloudinary_image = cloudinary.CloudinaryImage(id)

    original_image = cloudinary_image.image()

    # cloudinary_image = cloudinary.Cloudinary_image.image()




    return render_template('modified.html', id=id,original_image=original_image)
    # return redirect("/homepageaction")





#PROFILE PAGE
@app.route("/profilepageaction",methods=['GET'])
def profilepageaction():
    return redirect("/profilepage")

@app.route("/profilepage",methods=['GET'])
def profilepage():
    name = session['name'] 
    username = session['username']
    return render_template("profilepage.html",name=name,username=username)




#FOLLOWING AND FOLLOWERS PAGE
@app.route("/followingpageaction",methods=['GET'])
def followingpageaction():
    return redirect("/followingpage")

@app.route("/followingpage",methods=['GET'])
def followingepage():
    return render_template("followingpage.html")

@app.route("/followerspageaction",methods=['GET'])
def followerspageaction():
    return redirect("/followerspage")

@app.route("/followerspage",methods=['GET'])
def followersepage():
    return render_template("followerspage.html")





if __name__ == '__main__':
    # Import the variables from the .env file
    from dotenv import load_dotenv
    # Start the server
    app.run(debug=True)
