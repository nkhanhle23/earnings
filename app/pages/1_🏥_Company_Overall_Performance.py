import streamlit as st
import pandas as pd
import requests
from datetime import datetime


@st.cache_data
@st.cache_resource

# Custom function to fetch data from the API
def fetch_data(query):
        # Fetch data from the API
        response = requests.get("https://www.dolthub.com/api/v1alpha1/nkhanhle23/earnings",params={'q':query})
        data = response.json()

        # Turn data into a Pandas DataFrame
        data = pd.DataFrame(data["rows"])
    
        # VARIABLES
        data['date'] = pd.to_datetime(data['date'])
        data['year'] = data['date'].dt.year
        

        return data


# Function to format numbers in a shortened form (e.g., 1M, 1B)
import math

millnames = ['', ' T', ' M', ' B', ' T']

def millify(n):
    if isinstance(n, pd.Series):
        return n.apply(millify)
    else:
        millidx = max(0, min(len(millnames) - 1, int(math.floor(0 if n == 0 else math.log10(abs(n)) / 3))))
        return '{:.2f}{}'.format(n / 10 ** (3 * millidx), millnames[millidx])

# ------ get company names ------
query_rank = '''SELECT * FROM `income_statement` ORDER BY `date` DESC, `act_symbol` ASC'''
data = fetch_data(query=query_rank)

# ------ FILTER ------
selected_company = st.selectbox("Select Company", options=data["act_symbol"].unique())


# ------ DATA ------

query_asset = f'''SELECT * FROM `balance_sheet_assets` WHERE `act_symbol` = '{selected_company}' AND `period` = 'Year' ORDER BY `date` DESC'''
data_asset = fetch_data(query=query_asset)
query_income = f'''SELECT * FROM `income_statement` WHERE `act_symbol` = '{selected_company}' AND `period` = 'Year' ORDER BY `date` DESC'''
data_income = fetch_data(query=query_income)
query_equity = f'''SELECT * FROM `balance_sheet_equity` WHERE `act_symbol` = '{selected_company}' AND `period` = 'Year' ORDER BY `date` DESC'''
data_equity = fetch_data(query=query_equity)
query_cashflow = f'''SELECT * FROM `cash_flow_statement` WHERE `act_symbol` = '{selected_company}' AND `period` = 'Year' ORDER BY `date` DESC'''
data_cashflow = fetch_data(query=query_cashflow)

# Merge the two dataframes
data = pd.merge(data_income, data_asset, on=['act_symbol', 'date', 'year','period'], how='inner')
data = pd.merge(data, data_equity, on=['act_symbol', 'date', 'year','period'], how='inner')
data = pd.merge(data, data_cashflow, on=['act_symbol', 'date', 'year','period'], how='inner')

# ------ Select year ------
selected_year = st.selectbox("Select Year (applied for Summarized Income Statement)", data["year"].unique())

# Change data type to numeric
data["sales"] = pd.to_numeric(data["sales"])
data["cost_of_goods"] = pd.to_numeric(data["cost_of_goods"])
data["net_income"] = pd.to_numeric(data["net_income_x"])
data["total_assets"] = pd.to_numeric(data["total_assets"])
data["average_shares"] = pd.to_numeric(data["average_shares"])
data["total_equity"] = pd.to_numeric(data["total_equity"])
data["net_cash_from_operating_activities"] = pd.to_numeric(data["net_cash_from_operating_activities"])




# Get the current year
current_year = int(datetime.now().year) - 1

#filtered_data = data.query("act_symbol in @selected_company")

# Filter data for current year and previous year
data_current_year = data[data['date'].dt.year == current_year]
data_previous_year = data[data['year'].astype(int) == current_year - 1]

# Check if earnings data for the current year is available
if data_current_year.empty:
    st.warning(f"Earnings for last year {current_year} for {selected_company} have not been released yet.")
else:
    # ------ DERIVED KPIs ------

    # Current year
    # Revenue growth rate
    revenue_current_year = data_current_year['sales'].sum().astype(float)
    revenue_previous_year = data_previous_year['sales'].sum().astype(float)
    revenue_growth_rate = (revenue_current_year - revenue_previous_year) / revenue_previous_year * 100 if revenue_previous_year else 0


    # Gross profit margin
    cost_of_revenue_current_year = data_current_year['cost_of_goods'].sum()
    gross_profit_current_year = revenue_current_year - cost_of_revenue_current_year
    gross_profit_margin = gross_profit_current_year / revenue_current_year * 100  if revenue_current_year else 0

    # Return on assets and return on equity
    total_assets_current_year = data[data['date'].dt.year == current_year]['total_assets'].sum()
    total_equity_current_year = data[data['date'].dt.year == current_year]['total_equity'].sum()

    net_profit_current_year = data_current_year['net_income'].sum()
    net_profit_margin = net_profit_current_year / revenue_current_year if revenue_current_year else 0

    return_on_assets = net_profit_current_year / total_assets_current_year *100 if total_assets_current_year else 0
    return_on_equity = net_profit_current_year / total_equity_current_year *100 if total_equity_current_year else 0

    # Operating cash flow margin
    operating_cash_flow_current_year = data['net_cash_from_operating_activities'].sum()
    operating_cash_flow_margin = operating_cash_flow_current_year / revenue_current_year *100 if revenue_current_year else 0


   # Calculate the metrics for the current year
    revenue_current_year = data_current_year['sales'].sum().astype(float)
    cost_of_revenue_current_year = data_current_year['cost_of_goods'].sum()
    gross_profit_current_year = revenue_current_year - cost_of_revenue_current_year
    net_profit_current_year = data_current_year['net_income'].sum()
    total_assets_current_year = data[data['year'] == current_year]['total_assets'].sum()
    total_equity_current_year = data[data['year'] == current_year]['total_equity'].sum()
    operating_cash_flow_current_year = data_current_year['net_cash_from_operating_activities'].sum()

    # Calculate the metrics for the previous year
    revenue_previous_year = data_previous_year['sales'].sum().astype(float)
    cost_of_revenue_previous_year = data_previous_year['cost_of_goods'].sum()
    gross_profit_previous_year = revenue_previous_year - cost_of_revenue_previous_year
    net_profit_previous_year = data_previous_year['net_income'].sum()
    total_assets_previous_year = data[data['year'] == current_year - 1]['total_assets'].sum()
    total_equity_previous_year = data[data['year'] == current_year - 1]['total_equity'].sum()
    operating_cash_flow_previous_year = data_previous_year['net_cash_from_operating_activities'].sum()

    # Calculate derived KPIs current year
    revenue_growth_rate = (revenue_current_year - revenue_previous_year) / revenue_previous_year * 100 if revenue_previous_year else 0
    gross_profit_margin = gross_profit_current_year / revenue_current_year * 100 if revenue_current_year else 0
    net_profit_margin = net_profit_current_year / revenue_current_year * 100 if revenue_current_year else 0
    return_on_assets = net_profit_current_year / total_assets_current_year * 100 if total_assets_current_year else 0
    return_on_equity = net_profit_current_year / total_equity_current_year * 100 if total_equity_current_year else 0
    operating_cash_flow_margin = operating_cash_flow_current_year / revenue_current_year * 100 if revenue_current_year else 0

    # Calculate derived KPIs 2 years ago
    revenue_2_year = data[data['date'].dt.year == current_year - 2]['sales'].sum().astype(float)
    gross_profit_2_year = revenue_2_year - data[data['date'].dt.year == current_year - 2]['cost_of_goods'].sum()
    net_profit_2_year = data[data['date'].dt.year == current_year - 2]['net_income'].sum()
    total_assets_2_year = data[data['year'].astype(int) == current_year - 2]['total_assets'].sum()
    total_equity_2_year = data[data['year'].astype(int) == current_year - 2]['total_equity'].sum()
    operating_cash_flow_2_year = data[data['date'].dt.year == current_year - 2]['net_cash_from_operating_activities'].sum()

    # Filter data for current year and previous year
    data_previous_year = data[data['date'].dt.year == current_year - 1]
    data_current_year = data[data['date'].dt.year == current_year]


    # Calculate derived KPIs previous year
    revenue_growth_rate_previous_year = (revenue_previous_year - revenue_2_year) / revenue_2_year * 100 if revenue_current_year else 0
    gross_profit_margin_previous_year = gross_profit_previous_year / revenue_previous_year * 100 if revenue_previous_year else 0
    net_profit_margin_previous_year = net_profit_previous_year / revenue_previous_year * 100 if revenue_previous_year else 0
    return_on_assets_previous_year = net_profit_previous_year / total_assets_previous_year * 100 if total_assets_previous_year else 0
    return_on_equity_previous_year = net_profit_previous_year / total_equity_previous_year * 100 if total_equity_previous_year else 0
    operating_cash_flow_margin_previous_year = operating_cash_flow_previous_year / revenue_previous_year * 100 if revenue_previous_year else 0


    # Create a DataFrame for the metrics comparison
    metrics_comparison = pd.DataFrame({
        "Metric": ["Net Profit Margin", "Revenue Growth Rate", "Gross Profit Margin",
                "Return on Assets (ROA)", "Return on Equity (ROE)", "Operating Cash Flow (OCF) Margin"],
        "Current Year": [f"{net_profit_margin:.2f}%", f"{revenue_growth_rate:.2f}%", f"{gross_profit_margin:.2f}%",
                        f"{return_on_assets:.2f}%", f"{return_on_equity:.2f}%", f"{operating_cash_flow_margin:.2f}%"],
      
        "Difference": [f"{net_profit_margin - net_profit_margin_previous_year:.2f}",
                    f"{revenue_growth_rate - revenue_growth_rate_previous_year:.2f}",
                    f"{gross_profit_margin - gross_profit_margin_previous_year:.2f}",
                    f"{return_on_assets - return_on_assets_previous_year:.2f}",
                    f"{return_on_equity - return_on_equity_previous_year:.2f}",
                    f"{operating_cash_flow_margin - operating_cash_flow_margin_previous_year:.2f}"
                    
                    ]
    })


# SUMMARY DATA FOR INCOME STATEMENT
filtered_data = data.query("act_symbol in @selected_company and year == @selected_year")

# Change data type to numeric
filtered_data["sales"] = pd.to_numeric(filtered_data["sales"])
filtered_data["cost_of_goods"] = pd.to_numeric(filtered_data["cost_of_goods"])
filtered_data["selling_administrative_depreciation_amortization_expenses"] = pd.to_numeric(filtered_data["selling_administrative_depreciation_amortization_expenses"])
filtered_data["non_operating_income"] = pd.to_numeric(filtered_data["non_operating_income"])
filtered_data["interest_expense"] = pd.to_numeric(filtered_data["interest_expense"])
filtered_data["investment_gains"] = pd.to_numeric(filtered_data["investment_gains"])
filtered_data["other_income"] = pd.to_numeric(filtered_data["other_income"])
filtered_data["income_taxes"] = pd.to_numeric(filtered_data["income_taxes"])



# Calculate the summarized income statement components
revenue = filtered_data["sales"].sum().astype(float)
cost_of_revenue = filtered_data["cost_of_goods"].sum().astype(float)
gross_profit = float(revenue - cost_of_revenue)
operating_expense = filtered_data["selling_administrative_depreciation_amortization_expenses"].sum().astype(float)
operating_income = float(gross_profit - operating_expense)
other_income_expenses = (filtered_data["non_operating_income"] + filtered_data["interest_expense"] +
                        filtered_data["investment_gains"] + filtered_data["other_income"]).astype(float)
income_before_tax = float(operating_income + other_income_expenses)
tax_income_expense = filtered_data["income_taxes"].sum().astype(float)
net_income = float(income_before_tax - tax_income_expense)

# Create a DataFrame for the summarized income statement components
summary_data = pd.DataFrame({
    "": ["Revenue", "(-) Cost of Revenue", "= Gross Profit", "(-) Operating Expense",
            "= Operating Income", "(+-) Other Income/Expenses", "= Income Before Tax",
            "(+-) Tax Income/Expense", "= Net Income"],
    selected_year: [revenue, cost_of_revenue, gross_profit, operating_expense, operating_income,
            other_income_expenses.sum(), income_before_tax, tax_income_expense, net_income]
},index=None)



# Format the numbers in a shortened form
summary_data[selected_year] = millify(summary_data[selected_year])


# ------ MAIN PAGE ------

st.title("🏥 COMPANY OVERALL PERFORMANCE")
st.markdown("This dashboard displays the overall performance of the selected company.")
st.write("This is inspired by [Financial Dashboard 📈](https://abeltavares-financial-dashboard-app-app-ozm3yd.streamlit.app/)")
# ------ DISPLAY ------


# Define columns for key metrics and Income Statement
col2, col3, col4 = st.columns((2,2,4))

# Display key metrics

with col2:
    
    st.metric(label="Revenue Growth Rate", value=f"{revenue_growth_rate:.2f}%", delta=f"{revenue_growth_rate - revenue_growth_rate_previous_year:.2f}")
    st.metric(label="Gross Profit Margin", value=f"{gross_profit_margin:.2f}%", delta=f"{gross_profit_margin - gross_profit_margin_previous_year:.2f}")
    st.metric(label="Net Profit Margin", value=f"{net_profit_margin:.2f}%", delta=f"{net_profit_margin - net_profit_margin_previous_year:.2f}")
with col3:
    
    st.metric(label="Return on Assets (ROA)", value=f"{return_on_assets:.2f}%", delta=f"{return_on_assets - return_on_assets_previous_year:.2f}")
    st.metric(label="Return on Equity (ROE)", value=f"{return_on_equity:.2f}%", delta=f"{return_on_equity - return_on_equity_previous_year:.2f}")
    st.metric(label="Operating Cash Flow (OCF) Margin", value=f"{operating_cash_flow_margin:.2f}%", delta=f"{operating_cash_flow_margin - operating_cash_flow_margin_previous_year:.2f}")

with col4: 
    
    
    # Display the summarized income statement components in a table
    st.write("#### Summarized Income Statement")
    st.table(summary_data)


# Additional information
st.markdown(
    """
    
    **👈 For more details about the company's financials, please select the desired tab on the left.** 
    """
)
