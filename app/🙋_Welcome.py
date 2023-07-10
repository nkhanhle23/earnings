import streamlit as st

# SET PAGE CONFIGURATION
st.set_page_config(page_title="Financial Dashboard", page_icon=":chart_with_upwards_trend:")


@st.cache_data(ttl=24*60*60)
@st.cache_resource(ttl=24*60*60)


# Welcome page
st.write("# Welcome to the Financial Dashboard! :chart_with_upwards_trend:")
st.write("## Team LAY: Le, Anna, Yagmur")
st.write("This is our EA for Big Data Project.")
st.write("Our aim is to build an interactive financial dashboard, where you can choose and check selected KPIs and get insights into the company's performance and health.")


# Navigation
st.write("### Navigation:")
st.write("👈 Use the sidebar on the left to navigate to different sections:")
st.write("- **Company Overall Performance:** Analyze the overall performance of the selected company.")
st.write("- **Rank Comparison:** Compare the performance of different companies in a ranking format.")
st.write("- **Income Statement:** Analyze the company's revenue, expenses, and net income over time.")
st.write("- **Balance Sheet Analysis:** Explore the company's assets, liabilities, and equity.")
st.write("- **Cashflow Analysis:** Examine the company's cash inflows and outflows.")
st.write("- **Outlook & Forecast:** Gain insights into the company's future outlook and financial forecast.")


# Additional information
st.markdown(
    """
    
    
    ### Want to learn more about the data?
    - Check out [Earnings Data](https://www.dolthub.com/repositories/post-no-preference/earnings)
    
    ### Want to learn more about the project?
    - Check out [Big Data Project](https://github.com/nkhanhle23/earnings)
    """
)
