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
#------ MAIN PAGE ------
st.title( "🏆 RANK COMPARISON")  
st.markdown("This page allows you to check the compare the ranks of the companies of your choice.")
st.write('PLease keep in mind that not every company has a rank.')

# ------ DATA ------
query_rank = '''SELECT * FROM `rank_score` ORDER BY `date` DESC, `act_symbol` ASC'''
data = fetch_data(query=query_rank)

# ------ FILTER ------ 
selected_company = st.multiselect("Select Company", 
                                options=data["act_symbol"].unique()
                                )

df_selection = data.query("act_symbol in @selected_company")
df_selection = df_selection[['act_symbol', 'value', 'growth', 'momentum', 'vgm','rank']]

# Check if DataFrame is empty
if df_selection.empty:
    st.warning("Data unavailable for this filter, please select something else.")

st.header(f"Companies' rank breakdown")


# Display the breakdown of the rank
# Create a new DataFrame for the breakdown of rank
columns = ['value','growth', 'momentum', 'vgm']

# Create a new DataFrame for the breakdown of rank

# Create a net chart
fig = go.Figure()

# Iterate over each row in the DataFrame
for index, row in df_selection.iterrows():
    # Extract the company symbol and rank values
    company_symbol = row['act_symbol']
    value_rank = row['value']
    growth_rank = row['growth']
    momentum_rank = row['momentum']
    vgm_rank = row['vgm']
    
    # Add a scatter trace for each rank value
    fig.add_trace(go.Scatterpolar(
        r=[value_rank, growth_rank, momentum_rank, vgm_rank, value_rank],
        theta=['Value', 'Growth', 'Momentum', 'VGM', 'Value'],
        fill='toself',
        name=company_symbol
    ))

# Set layout properties
fig.update_layout(
    polar=dict(
        radialaxis=dict(
            visible=True,
            range=[0, 6],
            categoryorder="category descending"  # Set the order of categories
        )
    ),
    showlegend=True
)

# Render the net chart using Streamlit
st.plotly_chart(fig)

# ------ DATA TABLE ------
st.dataframe(df_selection)