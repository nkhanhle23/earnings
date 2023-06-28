import streamlit as st
from PIL import Image
import urllib.request

# SET PAGE CONFIGURATION
# Download the image from the URL
image_url = "https://cdn-icons-png.flaticon.com/512/8234/8234015.png"
image_path = "icon.png"
urllib.request.urlretrieve(image_url, image_path)

# Open the image using PIL
img = Image.open(image_path)

# Set page configuration
st.set_page_config(page_title="Financial Dashboard", page_icon=":bar_chart:")
# Welcome page
st.write("# Welcome to the Financial Dashboard! :bar_chart:")
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
