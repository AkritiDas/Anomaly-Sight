
import os
import streamlit as st
from streamlit_option_menu import option_menu
import welcome as wel
import tests as test
import analysis as analyse
from dotenv import load_dotenv
load_dotenv()
USER = os.getenv("user")
PASS = os.getenv("password")
HOST = os.getenv("host")

st.set_page_config(
    page_title="Anomaly Detection",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state='expanded'

)
def authenticate(user_id, user_pass):
    if user_id == USER and user_pass == PASS:
        return True
    else:
        return False

def login():
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    col1, col2 = st.columns(2)
    st.sidebar.title("Login")
    user_id = st.sidebar.text_input("User ID")
    user_pass = st.sidebar.text_input("Password", type="password")
    with col1:
        submit_button = st.sidebar.button("Submit",use_container_width=False)
    with col2:
        logout_button = st.sidebar.button("Logout", type='primary',use_container_width=False) 

    if submit_button:
      if user_id and user_pass: 
          if authenticate(user_id, user_pass):
              st.session_state.logged_in = True
              st.sidebar.success("Login successful!")
              st.balloons()
          else:
              st.sidebar.error("Invalid credentials")
      else:
          st.sidebar.warning("Please enter both User ID and Password")


    if logout_button:
      st.session_state.logged_in = False

def streamlit_menu():
    with st.sidebar:
        if st.session_state.logged_in:
            selected = option_menu(
                menu_title="Main Menu",
                options=["Authentication", "Analysis", "Tests"],
                icons=["house", "book", "envelope"],
                menu_icon="cast",
                default_index=1, 
                styles={
                "nav-link-selected": {"background-color": "blue"},
                },
            )
        else:
            selected = option_menu(
                menu_title="Main Menu",
                options=["Authentication"],
                icons=["house"],
                menu_icon="cast",
                default_index=0,
                styles={
                "nav-link-selected": {"background-color": "blue"},
                },
            )
    return selected
    
login()
selected = streamlit_menu()
if selected == "Authentication":
    if not st.session_state.logged_in:
        wel.message()
        st.warning("You are Not Logged In")
    else:
        wel.message()
        st.success("You are Logged In")
elif selected == "Analysis":
    if not st.session_state.logged_in:
        st.warning("You need to be logged in to access Analysis. Go to [Authentication](#) page...")
        st.stop()
    else:
        st.title(f"{selected}")
        analyse.dash()
        analyse.plot_data()
elif selected == "Tests":
    if not st.session_state.logged_in:
        st.warning("You need to be logged in to access Tests. Go to [Authentication](#) page...")
        st.stop()
    else: 
        test.form()
        