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
query_eps = '''SELECT * FROM `eps_estimate` ORDER BY `date` DESC'''
data_eps = fetch_data(query=query_eps)

query_sales = '''SELECT * FROM `sales_estimate` ORDER BY `date` DESC'''
data_sales = fetch_data(query=query_sales)

st.title("🔮 OUTLOOK & FORECAST")
st.markdown("This dashboard provides an analysis of the newest estimates and outlook of a selected company.")
st.write("Not all companies have estimates.")

# ------ FILTER ------
selected_company = st.selectbox('Select Company', sorted(data_eps['act_symbol'].unique()), key='company_selection')

# Filter data based on selected company
filtered_data_eps = data_eps[data_eps['act_symbol'] == selected_company][:4]
filtered_data_sales = data_sales[data_sales['act_symbol'] == selected_company][:4]

#st.dataframe(filtered_data_eps)

# ------ CHART ------
# EPS 
fig_eps = go.Figure()
fig_eps.add_trace(go.Bar(x=filtered_data_eps['period'], y=filtered_data_eps['year_ago'], name = "Consensus Last Year"))
fig_eps.add_trace(go.Bar(x=filtered_data_eps['period'], y=filtered_data_eps['consensus'], name = "Consensus This Year"))
fig_eps.add_trace(go.Scatter(x=filtered_data_eps['period'], y=filtered_data_eps['high'], name = "High", mode='markers', marker=dict(symbol="triangle-up",
                                                                                                                                    size=10,
                                                                                                                                    color="green"
                                                                                                                                    )))

fig_eps.add_trace(go.Scatter(x=filtered_data_eps['period'], y=filtered_data_eps['low'], name = "Low", mode='markers', marker=dict(symbol="triangle-down",
                                                                                                                                    size=10,
                                                                                                                                    color="red")))
desired_order = ['Current Quarter', 'Next Quarter', 'Current Year', 'Next Year']
fig_eps.update_layout(
    xaxis = dict(categoryarray=desired_order),
    title = f"{selected_company} - Earnings per Share Forecast"
)

# Sales

fig_sales = go.Figure()

fig_sales.add_trace(go.Bar(x=filtered_data_sales['period'], y=filtered_data_sales['year_ago'], name="Consensus Last Year"))
fig_sales.add_trace(go.Bar(x=filtered_data_sales['period'], y=filtered_data_sales['consensus'], name="Consensus This Year"))
fig_sales.add_trace(go.Scatter(x=filtered_data_sales['period'], y=filtered_data_sales['high'], name="High",
                            mode='markers', marker=dict(symbol="triangle-up", size=10, color="green")))
fig_sales.add_trace(go.Scatter(x=filtered_data_sales['period'], y=filtered_data_sales['low'], name="Low",
                            mode='markers', marker=dict(symbol="triangle-down", size=10, color="red")))



fig_sales.update_layout(
    xaxis=dict(categoryarray=desired_order),
    title = f"{selected_company} - Sales Forecast"
)




# ------ DISPLAY -----
st.title('Forecast Analysis')
st.header(f'Company: {selected_company}')
st.plotly_chart(fig_sales)
st.plotly_chart(fig_eps)
