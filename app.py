import streamlit as st
import pandas as pd
import datetime
import plotly.express as px
from streamlit_option_menu import option_menu

# Set up session state
if "expenses" not in st.session_state:
    st.session_state["expenses"] = []

if "categories" not in st.session_state:
    st.session_state["categories"] = ["Food", "Transport", "Entertainment", "Utilities", "Other"]

# Title of the web app
st.title("Expense Tracker")

# Sidebar navigation
with st.sidebar:
    selected = option_menu("Main Menu", ["Add Expense", "View Expenses", "Manage Categories", "Analytics", "Settings"], 
                           icons=['house', 'table', 'list', 'bar-chart-line', 'gear'], menu_icon="cast", default_index=0)

# Add Expense
if selected == "Add Expense":
    st.header("Add Expense")
    
    # Input fields for the expense entry
    date = st.date_input("Date", datetime.date.today())
    category = st.selectbox("Category", st.session_state["categories"])
    description = st.text_input("Description")
    amount = st.number_input("Amount", min_value=0.0, format="%.2f")
    
    # Button to add the expense
    if st.button("Add Expense"):
        new_expense = {"Date": date, "Category": category, "Description": description, "Amount": amount}
        st.session_state["expenses"].append(new_expense)
        st.success("Expense added successfully!")

# View Expenses
elif selected == "View Expenses":
    st.header("View Expenses")
    if st.session_state["expenses"]:
        expenses_df = pd.DataFrame(st.session_state["expenses"])
        st.dataframe(expenses_df)
        
        # Option to download the data
        csv = expenses_df.to_csv(index=False).encode()
        st.download_button(label="Download as CSV", data=csv, file_name='expenses.csv', mime='text/csv')
    else:
        st.info("No expenses added yet.")

# Manage Categories
elif selected == "Manage Categories":
    st.header("Manage Categories")
    new_category = st.text_input("New Category")
    if st.button("Add Category"):
        st.session_state["categories"].append(new_category)
        st.success("Category added successfully!")
    
    if st.session_state["categories"]:
        st.write("Existing Categories:")
        for category in st.session_state["categories"]:
            st.write(category)

# Analytics
elif selected == "Analytics":
    st.header("Expense Analytics")
    if st.session_state["expenses"]:
        expenses_df = pd.DataFrame(st.session_state["expenses"])
        
        # Total expenses
        total_expense = expenses_df["Amount"].sum()
        st.write(f"### Total Expense: ${total_expense:.2f}")
        
        # Expense by category
        fig = px.pie(expenses_df, names='Category', values='Amount', title='Expenses by Category')
        st.plotly_chart(fig)
        
        # Expense over time
        fig2 = px.line(expenses_df, x='Date', y='Amount', title='Expenses Over Time')
        st.plotly_chart(fig2)
    else:
        st.info("No expenses to analyze yet.")

# Settings
elif selected == "Settings":
    st.header("Settings")
    monthly_limit = st.number_input("Set Monthly Limit", min_value=0.0, format="%.2f")
    days_in_month = (datetime.date.today().replace(day=28) + datetime.timedelta(days=4)).day
    daily_limit = monthly_limit / days_in_month if monthly_limit else 0
    st.write(f"Daily Limit: ${daily_limit:.2f}")

    if st.button("Save Settings"):
        st.session_state["monthly_limit"] = monthly_limit
        st.session_state["daily_limit"] = daily_limit
        st.success("Settings saved successfully!")

    # Show current settings
    if "monthly_limit" in st.session_state:
        st.write(f"Current Monthly Limit: ${st.session_state['monthly_limit']:.2f}")
    if "daily_limit" in st.session_state:
        st.write(f"Current Daily Limit: ${st.session_state['daily_limit']:.2f}")