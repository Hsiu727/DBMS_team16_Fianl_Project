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
    'password': '1234',  # Change this to your MySQL password
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
            if role == 'user':
                session['username'] = username
                return redirect("/main_page2") # commit this line after completing TODO # 2
            elif role =='manager':
                session['username'] = username
                return redirect("/management_page")
        else:
            flash("Invalid username or password", "error")
            return render_template("login2.html")
    return render_template("login2.html")

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

# Remove job from shopping cart
@app.route("/remove_from_cart/<int:job_id>", methods=["POST"])
def remove_from_cart(job_id):
    if 'username' not in session:
        flash("Please log in to manage your cart.", "error")
        return redirect("/")

    user_id = session.get('user_id')

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Delete the job from the shopping cart
        cursor.execute("DELETE FROM shopping_car WHERE user_id = %s AND Job_id = %s", (user_id, job_id))
        if cursor.rowcount > 0:
            conn.commit()
            flash("Job removed from your shopping cart!", "success")
        else:
            flash("Job not found in your cart.", "warning")
    except mysql.connector.Error as err:
        flash(f"Error: {err}", "danger")
    finally:
        cursor.close()
        conn.close()

    return redirect("/view_cart")


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

# management page 
@app.route("/management_page")
def home2():
    return render_template("management_page.html")



# create page
# for management to insert data into a database
@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        title = request.form.get('title')
        posting_location = request.form.get('posting_location')
        company_name = request.form.get('company_name')
        max_salary = request.form.get('max_salary')
        min_salary = request.form.get('min_salary')

        # Connect to the database
        conn = get_db_connection()
        cursor = conn.cursor()
        
        #update to query1 
        i = 0
        #first check if id was used
        while True:
            cursor.execute("SELECT Job_id FROM job_posting WHERE Job_id = %s", (str(i),))
            #print(cursor.fetchone())
            if cursor.fetchone() is None:
                break
            else:
                i = i + 1
        #update to job_posting table
        #update to salary table
        #update to query1
        cursor.execute("INSERT INTO job_posting (Title, Posting_location, Company_name, Job_id) VALUES (%s, %s, %s, %s)", (title, posting_location, company_name, str(i)))
        cursor.execute("INSERT INTO salary (Job_id, Max_salary, Min_salary) VALUES (%s, %s, %s)", (str(i), max_salary, min_salary))
        cursor.execute("INSERT INTO query1 (Title, location, company, Max_salary, Min_salary, Job_id) VALUES (%s, %s, %s, %s, %s, %s)", (title, posting_location, company_name, max_salary, min_salary, str(i)))
        conn.commit()
        
        #update to the original database
        
        cursor.close()
        conn.close()
        
        flash("Insert successfully", "success")
        return redirect("/management_page")  # Redirect to read page to display data
    

    return render_template('create.html', page_title="Create Page")


#read page
@app.route('/read')
def read():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    search_query = request.args.get('search')  # 修正為與 HTML 輸入欄一致
    if search_query:
        query = '''
            SELECT Title, location, company, Max_salary, Min_salary 
            FROM query1 
            WHERE Title LIKE %s OR company LIKE %s OR Max_salary LIKE %s OR Min_salary LIKE %s
            LIMIT 5
        '''
        cursor.execute(query, (f'%{search_query}%', f'%{search_query}%', f'%{search_query}%', f'%{search_query}%'))
        results = cursor.fetchall()
    else:
        cursor.execute('SELECT Title, location, company, Max_salary, Min_salary FROM query1 ORDER BY Job_id LIMIT 5')
        results = cursor.fetchall()

        
    # 最近 5 条记录逻辑
    cursor.execute('SELECT Title, location, company, Max_salary, Min_salary FROM query1 ORDER BY Job_id LIMIT 5')
    latest_data = cursor.fetchall()

    conn.close()
    return render_template('read.html', page_title="Read Page", data=results, latest_data=latest_data)


#update
@app.route('/update', methods=['GET', 'POST'])
def update():
    conn = get_db_connection()
    cursor = conn.cursor()

    if request.method == 'POST':
        # 更新數據
        field = request.form['field']
        new_value = request.form['new_value']
        search = request.args.get('search')

        query = f"UPDATE query1 SET {field} = %s WHERE Title = %s OR Job_id = %s"
        cursor.execute(query, (new_value, search, search))
        conn.commit()
        flash(f"Successfully updated {field} to {new_value}.", "success")

    elif request.method == 'GET':
        # 查詢數據
        search = request.args.get('search')
        if search:
            cursor.execute("SELECT * FROM query1 WHERE Title = %s OR Job_id = %s", (search, search))
            data = cursor.fetchone()
        else:
            data = None

    conn.close()
    return render_template('update.html', page_title="Update Page", data=data)


@app.route('/delete', methods=['GET', 'POST'])
def delete():
    conn = get_db_connection()
    cursor = conn.cursor()

    if request.method == 'POST':
        job_id = request.form.get('job_id')
        # 刪除資料
        cursor.execute("DELETE FROM query1 WHERE Job_id = %s", (job_id,))
        cursor.execute("DELETE FROM benefits WHERE Job_id = %s", (job_id,))
        cursor.execute("DELETE FROM salary WHERE Job_id = %s", (job_id,))
        conn.commit()
        flash(f"Job with ID {job_id} has been deleted successfully.", "success")
        return redirect('/delete')

    search_query = request.args.get('search_query')
    data = []

    if search_query:
        # 搜尋資料
        query = '''
            SELECT Title, company, location, Max_salary, Min_salary, Job_id 
            FROM query1 
            WHERE Title LIKE %s OR company LIKE %s
        '''
        search_term = f"%{search_query}%"
        cursor.execute(query, (search_term, search_term))
        data = cursor.fetchall()

    cursor.close()
    conn.close()

    # 將搜尋結果傳遞給模板
    formatted_data = [
        {
            "Title": row[0],
            "company": row[1],
            "location": row[2],
            "Max_salary": row[3],
            "Min_salary": row[4],
            "Job_id": row[5],
        }
        for row in data
    ]
    return render_template('delete.html', page_title="Delete Page", data=formatted_data)


if __name__ == "__main__":
    app.run(debug=True)


