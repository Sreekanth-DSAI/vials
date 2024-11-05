"""
Explanation of the Code:

1. This file contains custom CSS styles that are applied to the Streamlit app for a more polished and user-friendly interface.
2. The `apply_styles` function injects HTML and CSS into the Streamlit app using the `st.markdown` function with the `unsafe_allow_html` flag.
3. Key style modifications:
    - Centers the main content inside the application window using flexbox (`.css-18e3th9` class).
    - Styles the login box, including background color, padding, border radius, and shadow for a card-like effect (`.login-box` class).
    - Reduces the size of the logo image inside the login box and adds margin (`.login-box img`).
    - Adjusts the size and margin of input elements such as select boxes, text inputs, and buttons to span the full width and have spacing between them.
    - Styles the login button to make it stand out with a red background and white text (`.login-box .stButton button`).
4. The styles ensure a more responsive and visually appealing layout by targeting specific Streamlit elements.
"""

import streamlit as st

def apply_styles():
    """
    Function to apply custom CSS styles for the Streamlit app. 
    It centers the content, styles the login box, adjusts input element widths, 
    and modifies button appearance.
    """
    st.markdown(
        """
        <style>
        /* Center the content inside the main area */
        .css-18e3th9 {
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;  /* Full height of the viewport */
        }

        /* Style the login box */
        .login-box {
            background-color: #f4f4f4;  /* Light grey background for the box */
            padding: 20px;  /* Padding inside the box */
            border-radius: 10px;  /* Rounded corners */
            text-align: center;  /* Center the text inside the box */
            width: 100%;  /* Take full width */
            max-width: 400px;  /* Limit the width to 400px */
            margin: 0 auto;  /* Center the box */
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);  /* Subtle shadow effect */
        }

        /* Style the logo */
        .login-box img {
            width: 100px;  /* Reduce the logo size */
            margin-bottom: 15px;  /* Space below the logo */
        }

        /* Style the title */
        .login-box h2 {
            font-size: 20px;  /* Font size for the title */
            margin-bottom: 20px;  /* Space below the title */
        }

        /* Adjust the width of input elements */
        .login-box .stSelectbox, 
        .login-box .stTextInput, 
        .login-box .stButton {
            width: 100%;  /* Full width for inputs and buttons */
            margin-bottom: 10px;  /* Space between form elements */
        }

        /* Style the login button */
        .login-box .stButton button {
            width: 100%;  /* Full width button */
            background-color: #ff4b4b;  /* Red background for the button */
            color: white;  /* White text */
        }
        </style>
        """,
        unsafe_allow_html=True
    )
