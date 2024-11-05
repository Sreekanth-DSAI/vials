"""
Explanation of the Code:

1. This is a Streamlit-based application for detecting objects in images (vials and PFS - pre-filled syringes) and saving the results to a database.
2. The app provides two input options for users:
    - "Upload Files": Users can upload multiple image files from their local system.
    - "Use Camera": Users can capture images using a connected camera.
3. The app displays the username in the sidebar once the user is logged in and provides an option to log out.
4. Images are saved to three different folders:
    - `original_images`: Stores the uploaded or captured original images.
    - `processed_images`: Stores images after object detection is applied.
    - `combined_images`: Stores images where original and processed images are combined for visualization.
5. The code uses two pre-trained models (for detecting "Vials" and "PFS") and selects the one that gives the higher count for final processing.
6. The results, including the image name, model used, counts for vials and PFS, timestamp, and username, are displayed in a table format.
7. Results are stored in a SQL database using SQLAlchemy after processing, ensuring that all information is logged for future reference.
8. The app shows the final combined images with a caption indicating the model used, and the processed data is pushed to the SQL database.
"""

import streamlit as st
import os
from datetime import datetime
from PIL import Image
from detection_model import get_db, predict_and_draw, concatenate_images, models
import pandas as pd
import sqlalchemy
from auth import DATABASE_URL 

# Function for user detection page
def user_detection_page():
    if "username" not in st.session_state:
        st.error("Please log in first.")
        return
    
    username = st.session_state["username"]  # Retrieve username
    st.sidebar.title(f"Hi, {username}!")  # Display username
    
    # Sidebar for input options
    st.sidebar.header("Input Selection")
    option = st.sidebar.radio("Select Input Method", ("Upload Files", "Use Camera"))

    # Setup directories
    original_folder = "original_images"
    processed_folder = "processed_images"
    combined_folder = "combined_images"
    os.makedirs(original_folder, exist_ok=True)
    os.makedirs(processed_folder, exist_ok=True)
    os.makedirs(combined_folder, exist_ok=True)

    images = []
    image_names = []

    if option == "Upload Files":
        with st.sidebar.form("upload-form", clear_on_submit=True):
            uploaded_files = st.file_uploader("Choose images...", type=["jpg", "jpeg", "png"], accept_multiple_files=True)
            submitted = st.form_submit_button("Upload")

            if submitted and uploaded_files:
                for uploaded_file in uploaded_files:
                    image = Image.open(uploaded_file)
                    images.append(image)
                    image_names.append(uploaded_file.name)
                    original_image_path = os.path.join(original_folder, uploaded_file.name)
                    image.save(original_image_path)
    
    elif option == "Use Camera":
        with st.sidebar.form("camera-form", clear_on_submit=True):
            camera_image = st.camera_input("Capture Image")
            submitted = st.form_submit_button("Capture")

            if submitted and camera_image:
                image = Image.open(camera_image)
                images.append(image)
                image_names.append(f"camera_capture_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg")
                original_image_path = os.path.join(original_folder, image_names[-1])
                image.save(original_image_path)

    if st.sidebar.button("Logout"):
        # Reset session state and rerun to go back to the home page
        st.session_state["logged_in"] = False
        st.session_state["is_admin"] = False
        st.session_state["username"] = None
        st.rerun()

    results_list = []
    for image, image_name in zip(images, image_names):
        st.write(f"Processing image: {image_name}")

        # Predict and draw for both models
        processed_image_vials, counts_vials, timestamp_vials = predict_and_draw(image, models["Vials"])
        processed_image_pfs, counts_pfs, timestamp_pfs = predict_and_draw(image, models["PFS"])

        total_vials = counts_vials.get("VIAL", 0)
        total_pfs = counts_pfs.get("PFS", 0)

        if total_vials >= total_pfs:
            final_image = processed_image_vials
            model_used = "Vials"
            final_counts = {"PFS": 0, "VIAL": total_vials}
        else:
            final_image = processed_image_pfs
            model_used = "PFS"
            final_counts = {"PFS": total_pfs, "VIAL": 0}

        processed_image_path = os.path.join(processed_folder, image_name)
        final_image.save(processed_image_path)

        original_img = Image.open(os.path.join(original_folder, image_name))
        combined_image = concatenate_images(original_img, final_image)
        combined_image_path = os.path.join(combined_folder, image_name)
        combined_image.save(combined_image_path)

        st.image(combined_image, caption=f"Combined Image with {model_used} model", use_column_width=True)

        # Append results to the list
        results_list.append({
            "Image Name": image_name,
            "Model Used": model_used,
            "PFS Count": final_counts["PFS"],
            "VIAL Count": final_counts["VIAL"],
            "Timestamp": timestamp_vials,
            "Username": username  # Add username to the results
        })

    # Display results as a table
    if results_list:
        st.write("Detection Results:")
        results_df = pd.DataFrame(results_list)
        st.dataframe(results_df)

        # Push the DataFrame to the SQL database
        db = sqlalchemy.create_engine(DATABASE_URL)
        results_df.to_sql('detection', con=db, if_exists='append', index=False)

        st.success("Results successfully saved to the database.")

# Call the user detection page function
user_detection_page()
