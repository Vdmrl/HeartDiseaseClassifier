import streamlit as st
from auth import login, logout, register
from classifier import run_classifier

# Initialize session state variables.
if "access_token" not in st.session_state:
    st.session_state["access_token"] = None
if "auth_mode" not in st.session_state:
    st.session_state["auth_mode"] = "login"


def show_logout():
    if st.button("Logout"):
        token = st.session_state.get("access_token")
        if token:
            try:
                logout(token)
            except Exception as e:
                st.error(f"Logout failed: {e}")
        st.session_state.clear()
        st.success("Logged out successfully!")
        st.rerun()

def show_login():
    st.subheader("Login")
    username = st.text_input("Username (email)", key="login_username")
    password = st.text_input("Password", type="password", key="login_password")
    col1, col2, col3 = st.columns([1, 4, 1])
    try:
        with col1:
            if st.button("Login"):
                token = login(username, password)
                st.session_state["access_token"] = token
                st.success("Logged in successfully!")
                st.rerun()
    except Exception as e:
        st.error(f"Invalid email or password")
    # Provide a button/link to switch to registration
    with col3:
        if st.button("Registration", key="to_register"):
            st.session_state["auth_mode"] = "register"
            st.rerun()

def show_registration():
    st.subheader("Register")
    email = st.text_input("Email", key="register_email")
    password = st.text_input("Password", type="password", key="register_password")
    age = st.number_input("Age (optional)", min_value=0, step=1, key="register_age")
    col1, col2, col3 = st.columns([1, 0.5, 1])
    try:
        with col1:
            if st.button("Register"):
                register(email, password, age if age > 0 else None)
                st.success("Registered successfully! Please log in.")
                st.session_state["auth_mode"] = "login"
                st.rerun()
    except Exception as e:
        st.error(f"Registration failed. Wrong email or such user already exist")

    # Provide a button/link to switch to login
    with col3:
        if st.button("Already have an account? Login here", key="to_login"):
            st.session_state["auth_mode"] = "login"
            st.rerun()


st.title("Heart Disease Classifier")

# Authentication flow:
if not st.session_state["access_token"]:
    if st.session_state["auth_mode"] == "login":
        show_login()
    else:
        show_registration()

# Only load the classifier if the user is authenticated.
if st.session_state.get("access_token"):
    show_logout()
    try:
        run_classifier()  # Call the renamed classifier function
    except Exception as e:
        st.error(f"Error loading classifier: {e}")

