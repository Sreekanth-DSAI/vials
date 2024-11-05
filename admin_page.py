
"""
Explanation of the Code:

1. This Streamlit application serves as an admin dashboard for user management.
2. It allows admins to view a table of users or create new users.
3. The admin can select between two actions: showing users or creating a user.
4. The user data is fetched from a PostgreSQL database using SQLAlchemy.
5. A form is provided for creating a new user, which includes input fields for user details.
6. Upon form submission, the user is created, and appropriate messages are displayed.
7. A logout button resets session state to navigate back to the home page.
"""

import streamlit as st
from auth import create_user, get_db
from styles import apply_styles
import pandas as pd
from sqlalchemy import text

def fetch_users(db_session):
    """Fetch users from the database using SQLAlchemy."""
    query = "SELECT employee_id, first_name, last_name, email, mobile_contact FROM users"
    
    # Execute the query using the session and fetch the results
    result = db_session.execute(text(query))
    users = result.fetchall()
    
    # Convert the result to a Pandas DataFrame
    users_df = pd.DataFrame(users, columns=["employee_id", "first_name", "last_name", "email", "mobile_contact"])
    return users_df

def admin_dashboard():
    # Apply custom styles if needed
    apply_styles()

    # Display the logo and title in the sidebar
    with st.sidebar:
        st.image("aispry.webp", width=150)  # Adjust width as needed for the sidebar
        st.markdown("<h2>Admin Dashboard</h2>", unsafe_allow_html=True)

    # Buttons for different admin functionalities
    st.write("## Admin Actions")

    # Radio button to select action
    action = st.radio("Select Action", ("Show Users Table", "Create User"))

    if action == "Show Users Table":
        st.subheader("Users Table")

        # Fetch users from the database and display them
        db = get_db()  # Get the session (assuming SQLAlchemy session)
        try:
            users = fetch_users(db)  # Fetch users from the database
            if not users.empty:
                st.dataframe(users)  # Display the fetched users in a table format
            else:
                st.info("No users found in the database.")  # Inform if no users exist
        except Exception as e:
            st.error(f"Error fetching users: {str(e)}")  # Display error if fetching fails

    elif action == "Create User":
        st.subheader("Create New User")

        # Form to create new users
        with st.form("create_user_form"):
            st.write("**Fill in the details to create a new user:**")
            employee_id = st.text_input("Employee ID")
            first_name = st.text_input("First Name")
            last_name = st.text_input("Last Name")
            username = st.text_input("Username")
            email = st.text_input("Email")
            mobile_contact = st.text_input("Mobile Contact")
            submit = st.form_submit_button("Create User")

            if submit:
                # Validate that all fields are filled
                if not employee_id or not first_name or not last_name or not email or not mobile_contact:
                    st.error("Please fill all the fields.")  # Error message for empty fields
                else:
                    db = get_db()  # Get the database session
                    try:
                        # Attempt to create a new user
                        create_user(db, employee_id, first_name, last_name, email, mobile_contact)
                        st.success(f"User {first_name} {last_name} created successfully!")  # Success message
                    except Exception as e:
                        st.error(f"Error creating user: {str(e)}")  # Display error if creation fails

    # Logout button
    if st.button("Logout"):
        # Reset session state and rerun to go back to the home page
        st.session_state["logged_in"] = False
        st.session_state["is_admin"] = False
        st.rerun()  # Rerun the app to refresh the state
