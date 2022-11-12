import psycopg2 
from flask import Flask, make_response, render_template, request, redirect,session,url_for
import bcrypt
import cloudinary
import cloudinary.uploader
import os

DB_URL = os.environ.get('DATABASE_URL', 'dbname=instanam')

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
    logged_name = session['name'] 
    username = session['username']

    posts = []

    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()

    display_photos = cur.execute('SELECT * FROM users_post')
    display_photos = cur.fetchall()
    
    

    for row in display_photos:
        image_id,name,img_url,description,like_counter = row
        posts.append([image_id,name,img_url,description,like_counter])

  

    

    cur.close()
    conn.close()
    
    return render_template("homepage.html",name=logged_name,username=username,posts=posts)
    


#LOGIN/LOGOUT
@app.route("/loginpageaction", methods=['POST'])
def loginpageaction():
    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()
    
    username = request.form['username']    
    password = request.form['password']
    print(password)


    hashed_password = cur.execute(f'SELECT password_hash FROM users WHERE username = %s', [username])
    hashed_password, = cur.fetchone()
    print(hashed_password)
    # if hashed_password is None:
    #     session['incorrect'] = "Incorrect Username or Password"
    #     return redirect('/')

    print(password)
    valid = bcrypt.checkpw(password.encode(), hashed_password.encode())
    
    if valid:
        print("match")
        cur.execute(f'SELECT id,name,username FROM users WHERE username = %s', [username])
        user_reccord = cur.fetchone()
        user_id,name,username = user_reccord
       
        session['id'] = user_id
        session['name'] = name
        session['username'] = username
        cur.close()
        conn.close()
        return redirect("/homepage")
    else:
        print("wrong password")
        session['incorrect'] = "Incorrect Username or Password"
        
        return redirect('/')


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
    conn = psycopg2.connect(DB_URL)
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
# @app.route("/displayuserspage")
# def displayuserspage():
#     # name = session['searched_name']
#     # username = session['searched_username']
#     # return render_template('/displayuserspage.html', name = name,username=username)
#     return render_template('/displayuserspage.html')


@app.route("/displayuserspageaction",methods=['POST'])
def displayuserspageaction():
    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()
    searched = request.form.get('search')
    users = []
    print(searched)
    # result = cur.execute('SELECT name,username FROM users WHERE username LIKE 'pop% )
    result = cur.execute("SELECT id,name,username FROM users WHERE username LIKE '%%' || %s || '%%' ", [searched])
    # "select * from table where {} like '%%' || %s || '%%'"
    # result = cur.execute( 'SELECT name FROM users')
    result = cur.fetchall()
    print(result)
    

    
    for row in result:
        id,name,username = row
        users.append([id,name,username])
        
  
    print("hello")
    # session['searched_username'] = username
    # session['sear']


    cur.close()
    conn.close()


    return render_template('/displayuserspage.html',users = users)




#POST IMAGE PAGE
@app.route("/postimagepage",methods=['POST'])
def postimagepage():
    return render_template("postimagepage.html")

@app.route("/postimagepageaction", methods=['POST'])
def postimagepageaction():
    image = request.files['image']
    response = cloudinary.uploader.upload(image, filename=image.filename)
    
    image_id = response['public_id']

    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()

    # user_id = session['user_id']
    name = session['name']
    description = request.form.get('description')
    cloudinary_image = cloudinary.CloudinaryImage(image_id)
    # img_url = cloudinary_image.image()
    img_url = cloudinary_image.build_url()
    cur.execute('INSERT INTO users_post (image_id,name,img_url,description) VALUES (%s, %s, %s, %s)', [image_id,name,img_url,description])
    print(img_url)

    conn.commit()
    cur.close()
    conn.close()
    
    return redirect("/homepage")






#PROFILE PAGE
@app.route("/profilepageaction",methods=['GET'])
def profilepageaction():
    # conn = psycopg2.connect(DB_URL)
    # cur = conn.cursor()

    # id = session['id']

    # posts = []
    # results = cur.execute(f'SELECT name,img_url,description FROM users_post WHERE id = %s', [id])

    # results = cur.fetchall()
    
    

    # for row in results:
    #     name,img_url,description = row
    #     posts.append([name,img_url,description])




    return redirect("/profilepage")

@app.route("/profilepage",methods=['GET'])
def profilepage():
    name = session['name'] 
    username = session['username']

    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor() 

   
    posts = []
    postss = []
    results = cur.execute(f'SELECT * FROM users_post WHERE name = %s', [name])

    results = cur.fetchall()
    
    

    for row in results:
        image_id,name,img_url,description,like_counter = row
        posts.append([image_id,name,img_url,description,like_counter])

    xd = cur.execute(f'SELECT follower_count,following_count FROM users WHERE name = %s', [name])

    xd = cur.fetchall()

    for follow in xd:
        follower_count,following_count = follow
        postss.append([follower_count,following_count])


    cur.close()
    conn.close()

    return render_template("profilepage.html",name=name,username=username,posts=posts,postss=postss)




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


@app.route("/followpageaction",methods=['GET'])
def followpageaction():
    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()   
    current_user = session['name']
    name = request.form.get('name')
    print(name)
    cur.execute('UPDATE users SET follower_count = follower_count + 1 WHERE name = %s',[name])
    cur.execute('UPDATE users SET following_count = following_count + 1 WHERE name = %s',[current_user])
    conn.commit()
    cur.close() 
    conn.close()
    
    return redirect('/viewprofilepage')


@app.route('/likebuttonaction',methods=['POST'])
def likebuttonaction():
    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()
    image_id = request.form.get('image_id')
    print(image_id)
    cur.execute('UPDATE users_post SET like_counter = like_counter + 1 WHERE image_id = %s',[image_id])
    conn.commit()
    cur.close() 
    conn.close()
    return redirect('/homepage')

@app.route('/commentaction',methods=['POST'])
def commentaction():
    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()
    name = session['name']
    username = session['username']
    comment = request.form.get('comment')
    image_id = request.form.get('image_id')

    cur.execute('INSERT INTO users_post (image_id,comments_name,comments_username,comments) VALUES (%s, %s, %s, %s)', [image_id,name,username,comment])
    
    conn.commit()
    cur.close() 
    conn.close()

    return redirect('/homepage')    



@app.route('/viewprofilepage',methods=['POST'])
def viewprofilepage():

    name = request.form.get('name')
    print(name)
    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()

    

    posts = []
    postss= []
    results = cur.execute(f'SELECT * FROM users_post WHERE name = %s', [name])

    results = cur.fetchall()
    
    

    for row in results:
        image_id,name,img_url,description,like_counter = row
        posts.append([image_id,name,img_url,description,like_counter])

    xd = cur.execute(f'SELECT follower_count,following_count FROM users WHERE name = %s', [name])

    xd = cur.fetchall()

    for follow in xd:
        follower_count,following_count = follow
        postss.append([follower_count,following_count])

    cur.close() 
    conn.close()


    
    return render_template("viewprofilepage.html",posts=posts,name=name,postss=postss)

@app.route('/displayallusers')
def displayallusers():
    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()
    
    users = []
    

    result = cur.execute('SELECT id,name,username FROM users')

    result = cur.fetchall()
 
    

    
    for row in result:
        id,name,username = row
        users.append([id,name,username])
        
  
    print("hello")
    # session['searched_username'] = username
    # session['sear']


    cur.close()
    conn.close()


    return render_template('/displayallusers.html',users = users)



if __name__ == '__main__':
    # Import the variables from the .env file
    from dotenv import load_dotenv
    # Start the server
    app.run(debug=True)



#following and followers list
#fix username login
#search bar result
#follow button
#clean css
#Like comment
