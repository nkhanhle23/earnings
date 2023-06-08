# app/views.py

from flask import render_template
from app import app, db
from app.models import IncomeStatement

@app.route('/')
def index():
    income_statements = IncomeStatement.query.all()
    return render_template('home.html', income_statements=income_statements)

@app.route('/')
def dashboard():
    # Fetch and process data for the dashboard
    # Pass the necessary data to the 'dashboard.html' template
    return render_template('dashboard.html', data=processed_data)

@app.route('/balance-sheet')
def balance_sheet():
    # Fetch data for the balance sheet report
    # Pass the necessary data to the 'balance_sheet.html' template
    return render_template('balance_sheet.html', data=balance_sheet_data)

@app.route('/filter', methods=['POST'])
def filter_reports():
    # Process filter parameters from the request
    # Fetch and filter data based on the parameters
    # Pass the filtered data to the appropriate templates for rendering
    return render_template('filtered_report.html', data=filtered_data)
