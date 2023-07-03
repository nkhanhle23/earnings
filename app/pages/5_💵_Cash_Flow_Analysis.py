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
query_cash_flow = '''SELECT * FROM `cash_flow_statement` ORDER BY `date` DESC, `act_symbol` ASC'''
data_cash_flow = fetch_data(query=query_cash_flow)


st.title("💵 CASH FLOW ANALYSIS")
st.write("This dashboard provides an analysis of the cash flow statement.")

# ------ FILTER ------
selected_company = st.selectbox('Select Company', data_cash_flow['act_symbol'].unique(), key='company_selection')
#selected_period = st.radio('Select Period', ('Quarter', 'Year'), key='period_selection')

# Select the relevant columns for cash flow chart
selected_columns_cash_flow = ['date', 'act_symbol', 'net_income', 'net_cash_from_operating_activities', 'net_cash_from_investing_activities', 'net_cash_from_financing_activities']

# Fetch cash flow data of the selected company from API
query_cash_flow = f'''SELECT * FROM `cash_flow_statement` WHERE `act_symbol` = '{selected_company}' ORDER BY `date` DESC'''
company_data_cash_flow = fetch_data(query=query_cash_flow)
df_selection_cash_flow = company_data_cash_flow[selected_columns_cash_flow]

# Change data type
df_selection_cash_flow['net_income'] = df_selection_cash_flow['net_income'].astype(float)
df_selection_cash_flow['net_cash_from_operating_activities'] = df_selection_cash_flow['net_cash_from_operating_activities'].astype(float)
df_selection_cash_flow['net_cash_from_investing_activities'] = df_selection_cash_flow['net_cash_from_investing_activities'].astype(float)
df_selection_cash_flow['net_cash_from_financing_activities'] = df_selection_cash_flow['net_cash_from_financing_activities'].astype(float)

# Plotting the cash flow breakdown chart
fig_cash_flow_breakdown = go.Figure()

for column in ['net_cash_from_operating_activities', 'net_cash_from_investing_activities', 'net_cash_from_financing_activities']:
    fig_cash_flow_breakdown.add_trace(go.Scatter(x=df_selection_cash_flow['date'], y=df_selection_cash_flow[column],
                                                mode='lines', name=column))

fig_cash_flow_breakdown.update_layout(xaxis=dict(title='Date'),
                                    yaxis=dict(title='Amount'),
                                    title=f"{selected_company} - Cash Flow Breakdown")


# Plotting the net income vs net cashflow from various activities chart

df_selection_cash_flow['sum_cashflow'] = df_selection_cash_flow['net_cash_from_operating_activities'] + df_selection_cash_flow['net_cash_from_investing_activities'] + df_selection_cash_flow['net_cash_from_financing_activities']
fig_net_income_vs_cash_flow = px.scatter(df_selection_cash_flow, x='net_income', y='sum_cashflow',
                                                labels={'net_income': 'Net Income', 'sum_cashflow': 'Net Cash from Activities'},
                                                title=f"{selected_company} - Net Income vs Cash Flow")

fig_net_income_vs_cash_flow.update_layout(
    xaxis=dict(title='Net Income'),
    yaxis=dict(title='Net Cash'),
)


# Display the cash flow chart
st.title('Cash Flow Analysis')
st.header(f'Company: {selected_company}')
st.plotly_chart(fig_net_income_vs_cash_flow)
st.plotly_chart(fig_cash_flow_breakdown)