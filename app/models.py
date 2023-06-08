# app/models.py

from app import db

class IncomeStatement(db.Model):
    __tablename__ = 'income_statement'

    # Define table columns as class variables
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)
    revenue = db.Column(db.Float)
    expenses = db.Column(db.Float)
    net_income = db.Column(db.Float)
    
    # Define any additional columns as needed
    
    def __repr__(self):
        return f'<IncomeStatement {self.id}>'
