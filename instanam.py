import psycopg2
from flask import Flask, make_response, render_template, request, redirect,session
import cloudinary
import cloudinary.uploader
import os
# CLOUDINARY_CLOUD = os.environ.get('CLOUDINARY_CLOUD')
# LOUDINARY_CLOUD = os.environ.get('CLOUDINARY_CLOUD')

# cloudinary.config(
#     cloud_name='CLOUDINARY_CLOUD',
#     api_key='',
#     api_secret='',

# )
# from models.db import sql_select

app = Flask(__name__)

app.config['SECRET_KEY'] = 'This is a pretend secret key'

@app.route("/")
def index():
    return render_template('loginpage.html')


@app.route("/homepageaction", methods=['POST'])
def homepageaction():
    return render_template("homepage.html")

@app.route("/signuppage")
def signuppage():
    return render_template("signuppage.html")

# @app.route("/signuppageaction", methods=['POST'])
# def signuppageaction():
#     return render_template("homepage.html")

@app.route("/displayuserspage",methods=['POST'])
def displayuserspage():
    return render_template("displayuserspage.html")

@app.route("/postimagepage",methods=['POST'])
def postimagepage():
    return render_template("postimagepage.html")

@app.route("/postimagepageaction",methods=['POST'])
def postimagepageaction():
    return redirect("/homepageaction")

@app.route("/profilepageaction",methods=['GET'])
def profilepageaction():
    return redirect("/profilepage")

@app.route("/profilepage",methods=['GET'])
def profilepage():
    return render_template("profilepage.html")





app.run(debug=True) 
