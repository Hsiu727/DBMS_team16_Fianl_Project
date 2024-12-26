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


