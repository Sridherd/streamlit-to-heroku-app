import streamlit as st
import pandas as pd
import os
import sqlite3
import smtplib
from email.mime.text import MIMEText

# Function to send email confirmation
def send_email(to_email, subject, body):
    from_email = "your-email@example.com"
    from_password = "your-email-password"

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = from_email
    msg['To'] = to_email

    server = smtplib.SMTP_SSL('smtp.example.com', 465)
    server.login(from_email, from_password)
    server.sendmail(from_email, to_email, msg.as_string())
    server.quit()

# Title
st.title("Data Science Alumni Event Registration Form")

# Load existing data from CSV if it exists
if os.path.isfile('alumni_registration.csv'):
    existing_data = pd.read_csv('alumni_registration.csv')
else:
    existing_data = pd.DataFrame(columns=['Name', 'Email', 'Phone', 'Graduation Year', 'Degree', 'Current Position', 'Company', 'LinkedIn', 'Interest in Speaking', 'Dietary Preferences'])
    st.warning("CSV file not found. Please create a new CSV file or restore the deleted file.")

# Collecting user details
name = st.text_input("Enter your full name:")
email = st.text_input("Enter your email address:")
phone = st.text_input("Enter your phone number:")
graduation_year = st.selectbox("Select your graduation year:", list(range(1980, 2024)))
degree = st.selectbox("Select your degree:", ["Bachelors", "Masters", "PhD"])
current_position = st.text_input("Enter your current position:")
company = st.text_input("Enter your current company:")
linkedin = st.text_input("Enter your LinkedIn profile URL:")
interest_in_speaking = st.radio("Are you interested in speaking at the event?", ["Yes", "No"])
dietary_preferences = st.text_area("Any dietary preferences or restrictions?")

# Submit button
if st.button("Submit"):
    # Check for duplicates
    if not existing_data.empty and email in existing_data['Email'].values:
        st.error("You have already registered for the event.")
    else:
        # Store the details in a dictionary
        data = {
            'Name': [name],
            'Email': [email],
            'Phone': [phone],
            'Graduation Year': [graduation_year],
            'Degree': [degree],
            'Current Position': [current_position],
            'Company': [company],
            'LinkedIn': [linkedin],
            'Interest in Speaking': [interest_in_speaking],
            'Dietary Preferences': [dietary_preferences]
        }

        # Convert dictionary to DataFrame
        df = pd.DataFrame(data)

        # Save DataFrame to CSV
        if not existing_data.empty:
            df.to_csv('alumni_registration.csv', mode='a', header=False, index=False)
        else:
            df.to_csv('alumni_registration.csv', mode='w', header=True, index=False)

        # Connect to the database (or create it if it doesn't exist)
        conn = sqlite3.connect('alumni_registration.db')
        c = conn.cursor()

        # Create table if it doesn't exist
        c.execute('''
            CREATE TABLE IF NOT EXISTS alumni (
                name TEXT,
                email TEXT,
                phone TEXT,
                graduation_year INTEGER,
                degree TEXT,
                current_position TEXT,
                company TEXT,
                linkedin TEXT,
                interest_in_speaking TEXT,
                dietary_preferences TEXT
            )
        ''')

        # Insert data into the table
        c.execute('''
            INSERT INTO alumni (name, email, phone, graduation_year, degree, current_position, company, linkedin, interest_in_speaking, dietary_preferences)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (name, email, phone, graduation_year, degree, current_position, company, linkedin, interest_in_speaking, dietary_preferences))

        # Commit the transaction
        conn.commit()

        # Close the connection
        conn.close()

        # Send email confirmation
        send_email(email, "Alumni Registration Confirmation", "Thank you for registering for the alumni event.")

        # Confirmation message
        st.write("### Your Details")
        st.write(f"**Full Name:** {name}")
        st.write(f"**Email Address:** {email}")
        st.write(f"**Phone Number:** {phone}")
        st.write(f"**Graduation Year:** {graduation_year}")
        st.write(f"**Degree:** {degree}")
        st.write(f"**Current Position:** {current_position}")
        st.write(f"**Current Company:** {company}")
        st.write(f"**LinkedIn Profile:** {linkedin}")
        st.write(f"**Interested in Speaking:** {interest_in_speaking}")
        st.write(f"**Dietary Preferences:** {dietary_preferences}")
        st.success("Your registration has been submitted successfully! A confirmation email has been sent.")
