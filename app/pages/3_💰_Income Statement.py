import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from datetime import datetime
import plotly.graph_objects as go


@st.cache_data
@st.cache_resource
def fetch_data(query):
    # Fetch data from the API
    response = requests.get("https://www.dolthub.com/api/v1alpha1/nkhanhle23/earnings",params={'q':query})
    data = response.json()

    # Turn data into a Pandas DataFrame
    data = pd.DataFrame(data["rows"])

    # VARIABLES
    data['date'] = pd.to_datetime(data['date'])
    data['year'] = data['date'].dt.year
    data['month'] = data['date'].dt.month

    return data

# ------ DATA ------
query = '''SELECT * FROM `income_statement` ORDER BY `date` DESC, `act_symbol` ASC'''
data = fetch_data(query=query)

# ------ TITLE ------
st.title("💰 INCOME STATEMENT")
st.write("The income statement is one of the three major financial statements that reports a company's financial performance over a specific accounting period. It tells you how much money a corporation made or lost.")

# ------ FILTER ------
selected_company = st.selectbox('Select Company', data['act_symbol'].unique(), key='company_selection')
selected_period = st.radio('Select Period', ('Quarter', 'Year'), key='period_selection')
# Select the relevant columns for the dashboard
selected_columns = ['act_symbol', 'date', 'sales', 'gross_profit', 'pretax_income', 'net_income']

# Fetch data of the selected company from API
query = f'''SELECT * FROM `income_statement` WHERE `act_symbol` = '{selected_company}' AND `period` = '{selected_period}' ORDER BY `date` DESC'''
company_data = fetch_data(query=query)
df_selection = company_data[selected_columns]

# Display the selected data
st.title('Company Performance Dashboard')
st.header(f'Company: {selected_company}')


# Line chart for sales over time
fig_sales = px.line(df_selection, x='date', y='sales', title='Sales Over Time')
st.plotly_chart(fig_sales)

# Bar chart for profit metrics
# Create a bar chart for gross profit
fig = go.Figure()
fig.add_trace(go.Bar(
    x=df_selection['date'],
    y=df_selection['gross_profit'],
    name='Gross Profit'
))

# Add lines for sales and net income
fig.add_trace(go.Scatter(
    x=df_selection['date'],
    y=df_selection['sales'],
    name='Sales',
    mode='lines',
    line=dict(color='blue', width=2)
))
fig.add_trace(go.Scatter(
    x=df_selection['date'],
    y=df_selection['net_income'],
    name='Net Income',
    mode='lines',
    line=dict(color='green', width=2)
))

# Customize the chart as needed
fig.update_layout(
    title='Profit Metrics by Date',
    xaxis_title='Date',
    yaxis_title='Amount',
    showlegend=True
)

# Display the chart
st.plotly_chart(fig)


# Bar chart for income metrics
fig_income = px.bar(df_selection, x='date', y='pretax_income', hover_data='net_income',
                    title='Pre-Tax Income and Net Income')
st.plotly_chart(fig_income)

# ------ DATA TABLE ------
st.dataframe(df_selection)