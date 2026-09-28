import streamlit as st
import pandas as pd
import os
import hashlib

# Path for user database
USER_DB = 'user_db.csv'

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def load_users():
    if os.path.exists(USER_DB):
        return pd.read_csv(USER_DB)
    else:
        return pd.DataFrame(columns=['username', 'password'])

def save_users(users_df):
    users_df.to_csv(USER_DB, index=False)

def register_user(username, password):
    users_df = load_users()
    if username in users_df['username'].values:
        return False, "Username already exists"
    new_user = pd.DataFrame({'username': [username], 'password': [hash_password(password)]})
    users_df = pd.concat([users_df, new_user], ignore_index=True)
    save_users(users_df)
    return True, "Registration successful"

def authenticate_user(username, password):
    users_df = load_users()
    user_row = users_df[users_df['username'] == username]
    if user_row.empty:
        return False
    stored_password = user_row['password'].iloc[0]
    return stored_password == hash_password(password)

def login_page():
    st.title("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    col1, col2 = st.columns(2)
    if col1.button("Login"):
        if authenticate_user(username, password):
            st.session_state['logged_in'] = True
            st.session_state['username'] = username
            st.success("Login successful!")
            st.rerun()
        else:
            st.error("Invalid username or password")
    if col2.button("Register"):
        st.session_state['show_register'] = True
        st.rerun()

def register_page():
    st.title("Register")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")
    col1, col2 = st.columns(2)
    if col1.button("Register"):
        if password != confirm_password:
            st.error("Passwords do not match")
        elif len(username) < 3 or len(password) < 6:
            st.error("Username must be at least 3 characters and password at least 6 characters")
        else:
            success, message = register_user(username, password)
            if success:
                st.success(message)
                st.session_state['show_register'] = False
                st.rerun()
            else:
                st.error(message)
    if col2.button("Back to Login"):
        st.session_state['show_register'] = False
        st.rerun()

def main():
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False
    if 'show_register' not in st.session_state:
        st.session_state['show_register'] = False

    if st.session_state['logged_in']:
        # Import and run the main app
        from app import main as app_main
        app_main()
    else:
        if st.session_state['show_register']:
            register_page()
        else:
            login_page()

if __name__ == "__main__":
    main()
