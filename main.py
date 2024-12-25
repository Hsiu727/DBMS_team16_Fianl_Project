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
@app.route("/",  methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        role = request.form.get('role')

        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        conn = get_db_connection()
        cursor = conn.cursor()
        
        if role == 'user':
            cursor.execute("SELECT password,id FROM users WHERE username = %s", (username,))
            result = cursor.fetchone()

        elif role == 'manager':
            cursor.execute("SELECT password,id FROM managers WHERE username = %s", (username,))
            result = cursor.fetchone()

        cursor.close()
        conn.close()

        if result==None:
            flash("Invalid username or password", "error")
            return render_template("login2.html")
        elif result[0] == hashed_password:
            # if pass the check, redirect to the welcome page and store the username in the session
            session['username'] = username
            session['user_id'] = result[1]
            return redirect("/main_page2") # commit this line after completing TODO # 2
        else:
            flash("Invalid username or password", "error")
            return render_template("login2.html")
    return render_template("login2.html")

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

# job_listings = [
#     {"title": "professor ", "company": "TechCorp", "location": "New York, NY", "salary": "$100k - $120k"},
#     {"title": "Marketing Specialist", "company": "MarketPlus", "location": "San Francisco, CA", "salary": "$60k - $80k"},
#     {"title": "Data Scientist", "company": "DataInsights", "location": "Remote", "salary": "$90k - $110k"},
#     {"title": "Graphic Designer", "company": "CreativeHub", "location": "Austin, TX", "salary": "$50k - $70k"},
#     {"title": "student", "company": "pung", "location": "nycu", "salary": "-30k~0k"},
# ]



@app.route("/main_page2")
def home():
    search_query = request.args.get('search_query')  # Get the search query from the URL
    
    conn = get_db_connection()
    cursor = conn.cursor()

    if search_query:  # If there's a search query, filter the jobs based on it
        query = """
        SELECT * FROM query1
        WHERE title LIKE %s OR company LIKE %s OR location LIKE %s
        LIMIT 21
        """
        search_term = f"%{search_query}%"
        cursor.execute(query, (search_term, search_term, search_term))
    else:
        # If no search query, get all jobs (or you can decide how to handle this)
        cursor.execute("SELECT * FROM query1 LIMIT 21")
    
    results = cursor.fetchall()
    cursor.close()
    conn.close()

    # Convert the results to a list of dictionaries
    job_listings = [{"title": row[0], "company": row[2], "location": row[1], "salary": f"{int(row[3])}~{int(row[4])}", "id":row[5]} for row in results]

    return render_template("main_page2.html", jobs=job_listings)

# Add job to shopping cart
@app.route("/add_to_cart/<int:job_id>", methods=["POST"])
def add_to_cart(job_id):
    if 'username' not in session:
        flash("Please log in to add jobs to your cart.", "error")
        return redirect("/")
    
    # Get the user ID from the session (this assumes you store user_id after login)
    user_id = session.get('user_id')


    # Connect to the database
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Insert the job into the shopping cart table
        cursor.execute("INSERT INTO shopping_car (user_id, Job_id) VALUES (%s, %s)", (user_id, job_id))
        conn.commit()
        flash("Job added to your shopping cart!", "success")
    except mysql.connector.Error as err:
        flash(f"Error: {err}", "danger")
    finally:
        cursor.close()
        conn.close()

    return redirect("/main_page2")

# View shopping cart
@app.route("/view_cart")
def view_cart():
    # Check if the user is logged in
    if 'username' not in session:
        return redirect("/")  # Redirect to login page if not logged in

    # Get user_id from session or database
    user_id = session['user_id']
    conn = get_db_connection()
    cursor = conn.cursor()

    # Get jobs added to the shopping cart for the user
    cursor.execute("""
    SELECT j.Job_id, j.Title, j.company, j.location, j.Min_salary, j.Max_salary 
    FROM shopping_car sc
    JOIN query1 j ON sc.Job_id = j.Job_id
    WHERE sc.user_id = %s
    """, (user_id,))
    
    cart_items = cursor.fetchall()
    cursor.close()
    conn.close()

    # Convert the results to a list of dictionaries
    job_listings_in_cart = [
        {
            "id": row[0],
            "title": row[1],
            "company": row[2],
            "location": row[3],
            "salary": f"{int(row[4])}~{int(row[5])}"
        }
        for row in cart_items
    ]

    return render_template("cart.html", cart_items=job_listings_in_cart)

@app.route("/company")
def company():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Get the current page number from the query string (default is 1)
    page = request.args.get("page", 1, type=int)
    per_page = 12  # Number of companies per page
    offset = (page - 1) * per_page  # Calculate the offset for SQL query

    # Fetch companies for the current page
    cursor.execute("""
    SELECT Company_name, State, Country, City, Address, URL 
    FROM company 
    LIMIT %s OFFSET %s
    """, (per_page, offset))
    companies = cursor.fetchall()

    # Fetch the total number of companies to calculate total pages
    cursor.execute("SELECT COUNT(*) FROM company")
    total_companies = cursor.fetchone()[0]
    total_pages = (total_companies + per_page - 1) // per_page  # Calculate total pages

    cursor.close()
    conn.close()

    # Define the range of page numbers to display (only 4 at a time)
    max_visible_pages = 4
    start_page = max(1, page - max_visible_pages // 2)
    end_page = min(total_pages, start_page + max_visible_pages - 1)

    if end_page - start_page + 1 < max_visible_pages:
        start_page = max(1, end_page - max_visible_pages + 1)

    page_range = range(start_page, end_page + 1)

    # Create a list of companies to pass to the template
    company_list = [
        {
            "Name": row[0],
            "State": row[1],
            "Countery": row[2],
            "City": row[3],
            "Address": row[4],
            "URL": row[5]
        }
        for row in companies
    ]

    return render_template(
        "company_page.html",
        jobs=company_list,
        page=page,
        total_pages=total_pages,
        page_range=page_range
    )



if __name__ == "__main__":
    app.run(debug=True)


