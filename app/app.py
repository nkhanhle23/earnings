# app.py

from flask import Flask, render_template, request
import mysql.connector
from config import DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_DATABASE

app = Flask(__name__)

# Connect to the Dolt database
db = mysql.connector.connect(
    host=DB_HOST,
    port=DB_PORT,
    user=DB_USER,
)

# Define a route and its handler
@app.route('/', methods=['GET'])
def index():
    # Fetch data from the database
    cursor = db.cursor()
    
    # Get filter values from the query parameters
    company_filter = request.args.get('company', '')
    date_filter = request.args.get('date', '')

    # Prepare the SQL query with filters
    query = "SELECT * FROM rank_score"
    conditions = []

    if company_filter:
        conditions.append(f"act_symbol = '{company_filter}'")
    if date_filter:
        conditions.append(f"date = '{date_filter}'")

    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    cursor.execute(query)
    ranks = cursor.fetchall()

    # Render the HTML template with the data and filters
    return render_template('index.html', ranks=ranks)

# Start the Flask application
if __name__ == '__main__':
    app.run()