"""
Explanation of the Code:

1. The Streamlit app is designed for vial and PFS detection and supports three types of logins: Admin, User, and Test User.
2. The app is modular, importing separate files (`styles`, `admin_page`, `user_page`, `auth`) for navigation and functionality:
    - `styles`: Applies custom styles like CSS to the app.
    - `admin_page`: Contains the admin dashboard logic and components.
    - `user_page`: Handles the user detection page logic.
    - `auth`: Manages user authentication (`authenticate`), database access (`get_db`), and test user creation (`create_test_user`).
3. The app checks if the user is logged in and dynamically shows the appropriate content based on the user's role (admin or regular user).
4. The app uses Streamlit's session state (`st.session_state`) to manage login status, role-based access control (admin or user), and to persist login information across different pages.
5. There are three login options:
    - **Admin Login:** Hardcoded admin credentials (`admin/admin`).
    - **User Login:** Authenticates against a backend function.
    - **Test User Login:** Logs in with predefined test credentials (`testuser@example.com/testpassword`).
6. Upon successful login, the user is redirected to the corresponding dashboard (admin or user detection page), using `st.rerun()` to refresh the page and display the new content.
7. The layout is centered using Streamlit's column layout, with the main content placed in the middle of the page.
"""

import streamlit as st

# Set page config as the very first Streamlit command
st.set_page_config(page_title="Detection App", page_icon="🔍", layout="wide")

# Importing modules for styles, admin page, user page, and authentication
from styles import apply_styles
from admin_page import admin_dashboard
from user_page import user_detection_page
from auth import authenticate, get_db, create_test_user

def home():
    """
    Main function to render the home page of the Streamlit app. 
    It handles login logic and dynamically displays either the 
    admin dashboard or the user detection page based on the user's login status.
    """
    # Apply custom styles (CSS or layout changes)
    apply_styles()

    # Initialize session state for login if not already set
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False
        st.session_state["is_admin"] = False  # Default to non-admin user

    # Center the content on the page by creating three columns (left, center, right)
    col_left, col_center, col_right = st.columns([1, 2, 1])

    # Center the login box within the middle column
    with col_center:
        # Create a container for the login box
        with st.container():
            # Display logo (reduced size) and the title of the app
            st.image("aispry.webp", use_column_width=False, width=200)
            st.markdown("<h2>Vial and PFS Detection App</h2>", unsafe_allow_html=True)

            # Ensure test user is created if it doesn't exist
            create_test_user()

            # Check if the user is already logged in
            if st.session_state["logged_in"]:
                # If logged in, show appropriate dashboard based on user role
                if st.session_state["is_admin"]:
                    admin_dashboard()  # Admin-specific page
                elif st.session_state["is_user"]:
                    user_detection_page()  # Regular user page
                else:
                    pass
                return  # Prevents login form from reappearing after login

            # Display login options for different roles
            option = st.selectbox(
                "Select Login Option",
                ["Admin Login", "User Login", "Test User Login"],
                key="login_option"
            )

            # Handle Admin Login
            if option == "Admin Login":
                # Input fields for admin credentials
                email = st.text_input("Admin Email", placeholder="admin@example.com")
                password = st.text_input("Password", type="password", placeholder="Password")
                if st.button("Login as Admin"):
                    # Simple check for hardcoded admin credentials
                    if email == "admin" and password == "admin":
                        st.session_state["logged_in"] = True
                        st.session_state["is_admin"] = True
                        st.session_state["is_user"] = False
                        st.rerun()  # Reload the page to show admin dashboard
                    else:
                        st.error("Invalid admin credentials!")  # Show error for incorrect login

            # Handle User Login
            elif option == "User Login":
                # Input fields for regular user credentials
                email = st.text_input("User Email", placeholder="user@example.com")
                password = st.text_input("Password", type="password", placeholder="Password")
                if st.button("Login as User"):
                    # Authenticate user using the `authenticate` function from auth module
                    user = authenticate(email, password)
                    if user:
                        st.session_state["logged_in"] = True
                        st.session_state["is_admin"] = False
                        st.session_state["is_user"] = True
                        st.rerun()  # Reload the page to show user detection page
                    else:
                        st.error("Invalid user credentials!")  # Show error for invalid credentials

            # Handle Test User Login
            elif option == "Test User Login":
                if st.button("Login as Test User"):
                    # Predefined credentials for test user
                    email = "testuser@example.com"
                    password = "testpassword"
                    # Authenticate the test user
                    user = authenticate(email, password)
                    if user:
                        st.session_state["logged_in"] = True
                        st.session_state["is_admin"] = False
                        st.session_state["is_user"] = True
                        st.session_state["username"] = "TestUser"  # Assign test user name
                        st.rerun()  # Reload the page to show user detection page
                    else:
                        st.error("Invalid test user credentials!")  # Handle login failure
            
            st.markdown("</div>", unsafe_allow_html=True)  # Closing div tag for HTML content

if __name__ == "__main__":
    home()  # Run the home function to launch the app
