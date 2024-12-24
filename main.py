from flask import Flask, render_template, request, redirect, flash, session
import mysql.connector
import hashlib

# Flask App Initialization
app = Flask(__name__)
app.secret_key = "your_secret_key"

# Database Configuration
db_config = {
    'host': 'localhost',  # Change this to your MySQL host
    'user': 'root',  # Change this to your MySQL username
    'password': '',  # Change this to your MySQL password
    'database': 'final_project'  # Change this to your MySQL database name
}

# Database Connection
def get_db_connection():
    return mysql.connector.connect(**db_config)

# Login Page
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']

        # TODO # 4: Hash the password using SHA-256
        # password = ???
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        # Connect to the database
        conn = get_db_connection()
        cursor = conn.cursor()

        # TODO # 2. Check if the user exists in the database and whether the password is correct
        # Query to check the user
        #cursor.execute(f"SELECT password FROM users WHERE username = '{username}'")
        cursor.execute("SELECT password FROM users WHERE username = %s", (username,))
        result = cursor.fetchone() # fetchone() returns None if no record is found
        
        # Close the connection
        cursor.close()
        conn.close()
        
        # if ???:
        if result==None:
            flash("Invalid username or password", "error")
            return render_template("login.html")
        elif result[0] == hashed_password:
            # if pass the check, redirect to the welcome page and store the username in the session
            session['username'] = username
            return redirect("/main_page") # commit this line after completing TODO # 2
        else:
            flash("Invalid username or password", "error")
            return render_template("login.html")
        
    return render_template("login.html")

# Welcome Page
@app.route("/welcome")
def welcome():
    if 'username' not in session:
        return redirect("/")
    return render_template("welcome.html")

# Logout
@app.route("/logout")
def logout():
    session.pop('username', None)
    return redirect("/")

# Signup
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']

        # TODO # 4: Hash the password using SHA-256
        # password = ???
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        # Connect to the database
        conn = get_db_connection()
        cursor = conn.cursor()



        # TODO # 3: Add the query to insert a new user into the database
        try:
            # Insert new user into the database
            cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, hashed_password))
            conn.commit()
            flash("Account created successfully! Please log in.", "success")
            return redirect("/")
        
        except mysql.connector.Error as err:
            flash(f"Error: {err}", "danger")
            
        finally:
            cursor.close()
            conn.close()
    
    return render_template("signup.html")

job_listings = [
    {"title": "Software Engineer", "company": "TechCorp", "location": "New York, NY", "salary": "$100k - $120k"},
    {"title": "Marketing Specialist", "company": "MarketPlus", "location": "San Francisco, CA", "salary": "$60k - $80k"},
    {"title": "Data Scientist", "company": "DataInsights", "location": "Remote", "salary": "$90k - $110k"},
    {"title": "Graphic Designer", "company": "CreativeHub", "location": "Austin, TX", "salary": "$50k - $70k"},
]

@app.route("/")
def home():
    return render_template("index.html", jobs=job_listings)

@app.route("/search", methods=["POST"])
def search():
    query = request.form.get("query", "").lower()
    filtered_jobs = [job for job in job_listings if query in job["title"].lower() or query in job["company"].lower()]
    return render_template("index.html", jobs=filtered_jobs)


if __name__ == "__main__":
    app.run(debug=True)


