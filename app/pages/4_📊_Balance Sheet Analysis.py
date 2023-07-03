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
query_equity = '''SELECT * FROM `balance_sheet_equity` ORDER BY `date` DESC, `act_symbol` ASC'''
data_equity = fetch_data(query=query_equity)

query_assets = '''SELECT * FROM `balance_sheet_assets` ORDER BY `date` DESC, `act_symbol` ASC'''
data_assets = fetch_data(query=query_assets)

query_liabilities = '''SELECT * FROM `balance_sheet_liabilities` ORDER BY `date` DESC, `act_symbol` ASC'''
data_liabilities = fetch_data(query=query_liabilities)

st.title("📊 BALANCE SHEET ANALYSIS")
st.write("This dashboard provides an analysis of the balance sheet, including equity, assets, and liabilities.")

# ------ FILTER ------
selected_company = st.selectbox('Select Company', data_equity['act_symbol'].unique(), key='company_selection')
selected_period = st.radio('Select Period', ('Quarter', 'Year'), key='period_selection')


# Select the relevant columns for equity chart
selected_columns_equity = ['date', 'act_symbol', 'common_stock', 'retained_earnings', 'total_equity']

# Fetch equity data of the selected company from API
query_equity = f'''SELECT * FROM `balance_sheet_equity` WHERE `act_symbol` = '{selected_company}' AND `period` = '{selected_period}' ORDER BY `date` DESC'''
company_data_equity = fetch_data(query=query_equity)
df_selection_equity = company_data_equity[selected_columns_equity]

# Plotting the equity chart
fig_equity = px.line(df_selection_equity, x='date', y=['common_stock', 'retained_earnings', 'total_equity'],
                    labels={'value': 'Amount', 'date': 'Date'},
                    title=f"{selected_company} - Equity")

fig_equity.update_layout(
    xaxis=dict(type='category'),
    yaxis=dict(title='Amount'),
    legend_title='Equity',
)

# Select the relevant columns for assets chart
selected_columns_assets = ['date', 'act_symbol', 'cash_and_equivalents', 'receivables', 'inventories', 'total_current_assets']

# Fetch assets data of the selected company from API
query_assets = f'''SELECT * FROM `balance_sheet_assets` WHERE `act_symbol` = '{selected_company}' AND `period` = '{selected_period}' ORDER BY `date` DESC'''
company_data_assets = fetch_data(query=query_assets)
df_selection_assets = company_data_assets[selected_columns_assets]

# Plotting the assets chart
fig_assets = px.line(df_selection_assets, x='date', y=['cash_and_equivalents', 'receivables', 'inventories', 'total_current_assets'],
                    labels={'value': 'Amount', 'date': 'Date'},
                    title=f"{selected_company} - Assets")

fig_assets.update_layout(
    xaxis=dict(type='category'),
    yaxis=dict(title='Amount'),
    legend_title='Assets',
)

# Select the relevant columns for liabilities chart
selected_columns_liabilities = ['date', 'act_symbol', 'notes_payable', 'accounts_payable', 'total_current_liabilities']
# Fetch assets data of the selected company from API
query_liabilities = f'''SELECT * FROM `balance_sheet_liabilities` WHERE `act_symbol` = '{selected_company}' AND `period` = '{selected_period}' ORDER BY `date` DESC'''
company_data_liabilities = fetch_data(query=query_assets)
df_selection_liabilities = company_data_assets[selected_columns_assets]

# Plotting the assets chart
fig_liabilities = px.line(df_selection_assets, x='date', y=['cash_and_equivalents', 'receivables', 'inventories', 'total_current_assets'],
                    labels={'value': 'Amount', 'date': 'Date'},
                    title=f"{selected_company} - Liabilities")

fig_assets.update_layout(
    xaxis=dict(type='category'),
    yaxis=dict(title='Amount'),
    legend_title='Assets',
)

# ------ DISPLAY ------
st.header(f'Company: {selected_company}')
st.plotly_chart(fig_equity)
st.plotly_chart(fig_assets)
st.plotly_chart(fig_liabilities)