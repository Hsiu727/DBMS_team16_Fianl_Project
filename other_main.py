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




if __name__ == "__main__":
    app.run(debug=True)


