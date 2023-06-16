# IMPORT PACKAGES
import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from datetime import datetime
import plotly.graph_objects as go
from PIL import Image
import urllib.request

def main():
    # SET PAGE CONFIGURATION
    # Download the image from the URL
    image_url = "https://cdn-icons-png.flaticon.com/512/8234/8234015.png"
    image_path = "icon.png"
    urllib.request.urlretrieve(image_url, image_path)

    # Open the image using PIL
    img = Image.open(image_path)

    # Set page configuration
    st.set_page_config(page_title="Financial Analysis", page_icon=img)
    
    # ------ DATA FUNCTION ------
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
    #  ------ SIDE BAR ------  
    # Create buttons for each page
    # Define emojis for each page
    emoji_about = "🏚️"
    emoji_health_check = "🏥"
    emoji_income_statement = "💰"
    emoji_balance_sheet = "📊"
    emoji_cash_flow = "💵"
    emoji_outlook_forecast = "🔮"

    # Create buttons with emojis for each page
    button_about = emoji_about + " Home Page"
    button_health_check = emoji_health_check + " Company Health Check"
    button_income_statement = emoji_income_statement + " Earnings Analysis"
    button_balance_sheet = emoji_balance_sheet + " Balance Sheet Analysis"
    button_cash_flow = emoji_cash_flow + " Cash Flow Analysis"
    button_outlook_forecast = emoji_outlook_forecast + " Outlook and Forecast"

    # Create a sidebar menu for navigation
    st.sidebar.title("Navigation")
    selection = st.sidebar.radio("Go to", [button_about, button_health_check, button_income_statement, button_balance_sheet, button_cash_flow, button_outlook_forecast])
    
    # ------ DASHBOARDS/WEB PAGES ------
    if selection == button_about:
        st.title(emoji_about + " HOME PAGE")
        st.write("We are a group of students from the Berlin School of Economics and Law.")
        st.write("We are currently working on a project to build a web application that allows users to check the financial performance of a company.")

    elif selection == button_health_check:  
        # ------ MAIN PAGE ------
        st.title(emoji_health_check + " COMPANY HEALTH CHECK")  
        st.markdown("This page allows you to check the company's performance based on its financials.")

        # ------ DATA ------
        query_rank = '''SELECT * FROM `rank_score` ORDER BY `date` DESC'''
        data = fetch_data(query=query_rank)

        # ------ FILTER ------ 
        selected_company = st.multiselect("Select Company", 
                                        options=data["act_symbol"].unique()
                                        )
        
        df_selection = data.query("act_symbol in @selected_company")
        df_selection = df_selection[['act_symbol', 'value', 'growth', 'momentum', 'vgm']]

        # Check if DataFrame is empty
        if df_selection.empty:
            st.write("Data unavailable for this filter, please select something else.")

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

    elif selection == button_income_statement:
        
        # ------ DATA ------
        query = '''SELECT * FROM `income_statement` ORDER BY `date` DESC'''
        data = fetch_data(query=query)

        # ------ TITLE ------
        st.title(emoji_income_statement + " EARNINGS ANALYSIS")
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

    elif selection == button_balance_sheet:
        
        # ------ DATA ------
        query_equity = '''SELECT * FROM `balance_sheet_equity` ORDER BY `date` DESC'''
        data_equity = fetch_data(query=query_equity)

        query_assets = '''SELECT * FROM `balance_sheet_assets` ORDER BY `date` DESC'''
        data_assets = fetch_data(query=query_assets)

        query_liabilities = '''SELECT * FROM `balance_sheet_liabilities` ORDER BY `date` DESC'''
        data_liabilities = fetch_data(query=query_liabilities)

        st.title(emoji_balance_sheet + " BALANCE SHEET ANALYSIS")
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



    elif selection == button_cash_flow:
        # ------ DATA ------
        query_cash_flow = '''SELECT * FROM `cash_flow_statement` ORDER BY `date` DESC'''
        data_cash_flow = fetch_data(query=query_cash_flow)


        st.title(emoji_cash_flow + " CASH FLOW ANALYSIS")
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
        
        

    elif selection == button_outlook_forecast:
        # ------ DATA ------
        query_eps = '''SELECT * FROM `eps_estimate` ORDER BY `date` DESC'''
        data_eps = fetch_data(query=query_eps)

        query_sales = '''SELECT * FROM `sales_estimate` ORDER BY `date` DESC'''
        data_sales = fetch_data(query=query_sales)

        st.title(emoji_outlook_forecast + " OUTLOOK & FORECAST")
        st.write("This dashboard provides an analysis of the newest estimates and outlook of a selected company.")

        # ------ FILTER ------
        selected_company = st.selectbox('Select Company', data_eps['act_symbol'].unique(), key='company_selection')

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
        st.plotly_chart(fig_eps)
        st.plotly_chart(fig_sales)

if __name__ == "__main__":
    main()