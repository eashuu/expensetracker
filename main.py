import streamlit as st
import pandas as pd
import datetime
import plotly.express as px
from db import create_user, get_user

def main():
    st.title("Expense Tracker")

    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False

    if not st.session_state['logged_in']:
        login_signup()
    else:
        expense_tracker()

def login_signup():
    st.sidebar.title("Login / Signup")

    menu = ["Login", "Signup"]
    choice = st.sidebar.selectbox("Select Option", menu)

    if choice == "Login":
        st.subheader("Login")

        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            user = get_user(username)
            if user and user['password'] == password:
                st.success("Logged in as {}".format(username))
                st.session_state['logged_in'] = True
                st.session_state['username'] = username
                st.experimental_rerun()
            else:
                st.error("Invalid Username or Password")

    elif choice == "Signup":
        st.subheader("Signup")

        new_username = st.text_input("Username")
        new_password = st.text_input("Password", type="password")

        if st.button("Signup"):
            if new_username and new_password:
                if get_user(new_username):
                    st.warning("Username already exists")
                else:
                    create_user(new_username, new_password)
                    st.success("You have successfully created an account")
                    st.info("Go to Login Menu to login")
            else:
                st.error("Please provide a valid username and password")

def expense_tracker():
    with st.sidebar:
        selected = st.selectbox("Main Menu", ["Add Expense", "View Expenses", "Manage Categories", "Analytics", "Settings", "Logout"])

    if selected == "Logout":
        st.session_state['logged_in'] = False
        st.experimental_rerun()

    # Add Expense
    if selected == "Add Expense":
        st.header("Add Expense")

        # Input fields for the expense entry
        date = st.date_input("Date", datetime.date.today())
        category = st.selectbox("Category", st.session_state.get("categories", ["Food", "Transport", "Entertainment", "Utilities", "Other"]))
        description = st.text_input("Description")
        amount = st.number_input("Amount", min_value=0.0, format="%.2f")

        # Button to add the expense
        if st.button("Add Expense"):
            new_expense = {"Date": date, "Category": category, "Description": description, "Amount": amount}
            if "expenses" not in st.session_state:
                st.session_state["expenses"] = []
            st.session_state["expenses"].append(new_expense)
            st.success("Expense added successfully!")

    # View Expenses
    elif selected == "View Expenses":
        st.header("View Expenses")
        if st.session_state.get("expenses"):
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
            if "categories" not in st.session_state:
                st.session_state["categories"] = []
            st.session_state["categories"].append(new_category)
            st.success("Category added successfully!")

        if st.session_state.get("categories"):
            st.write("Existing Categories:")
            for category in st.session_state["categories"]:
                st.write(category)

    # Analytics
    elif selected == "Analytics":
        st.header("Expense Analytics")
        if st.session_state.get("expenses"):
            expenses_df = pd.DataFrame(st.session_state["expenses"])

            # Total expenses
            total_expense = expenses_df["Amount"].sum()
            st.write(f"### Total Expense: Rs{total_expense:.2f}")

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
        st.write(f"Daily Limit: {daily_limit:.2f}Rs")

        if st.button("Save Settings"):
            st.session_state["monthly_limit"] = monthly_limit
            st.session_state["daily_limit"] = daily_limit
            st.success("Settings saved successfully!")

        # Show current settings
        if "monthly_limit" in st.session_state:
            st.write(f"Current Monthly Limit: Rs{st.session_state['monthly_limit']:.2f}")
        if "daily_limit" in st.session_state:
            st.write(f"Current Daily Limit: Rs{st.session_state['daily_limit']:.2f}")

if __name__ == "__main__":
    main()