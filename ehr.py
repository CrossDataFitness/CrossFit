import streamlit as st
import pandas as pd
import plotly.express as px
import itertools
import numpy as np
from pycaret.regression import setup, create_model, finalize_model, predict_model
from ehr_db import create_table, add_data,add_user, create_user,view_all_data,view_all_users, view_all_data_names, get_name, edit_name_data, delete_data
from streamlit.components.v1 import html
create_user()
    

def nav_page(page_name, timeout_secs=3):
    nav_script = """
        <script type="text/javascript">
            function attempt_nav_page(page_name, start_time, timeout_secs) {
                var links = window.parent.document.getElementsByTagName("a");
                for (var i = 0; i < links.length; i++) {
                    if (links[i].href.toLowerCase().endsWith("/" + page_name.toLowerCase())) {
                        links[i].click();
                        return;
                    }
                }
                var elasped = new Date() - start_time;
                if (elasped < timeout_secs * 1000) {
                    setTimeout(attempt_nav_page, 100, page_name, start_time, timeout_secs);
                } else {
                    alert("Unable to navigate to page '" + page_name + "' after " + timeout_secs + " second(s).");
                }
            }
            window.addEventListener("load", function() {
                attempt_nav_page("%s", new Date(), %d);
            });
        </script>
    """ % (page_name, timeout_secs)
    html(nav_script)
sign_in = ''
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.header("Welcome to CrossData 🏋️‍")
user_name = st.text_input("Enter your user name")
password = st.text_input("Enter your password")

login_btn = st.button("Log In")
if login_btn:
    result = view_all_users()
    df = pd.DataFrame(result, columns=['user_name', 'password'])
    user_check_df = df[df['user_name'] == user_name]
    try:
        if user_check_df['password'].iloc[-1] == password:
            add_user(user_name, password)
            nav_page("display")
        else:
            st.error("Incorrect password or user name. Please try again.")
    except:
        st.error("Incorrect password or user name. Please try again.")
account_btn = st.button("Create Account")
if account_btn:
    result1 = view_all_users()
    df1 = pd.DataFrame(result1, columns=['user_name', 'password'])
    user_check_df1 = df1[df1['user_name'] == user_name]
    if len(user_check_df1) < 1:
        
        add_user(user_name, password)
        st.info("Welcome " + user_name + " please proceed to login in with your new acount.")
    else:
        st.error("User Name Taken. If you already have an account, please enter your user name and select log in. If you are a new user, please enter a new user name.")
forgot_password = st.button("Change Password")
if forgot_password:
    st.info("Please reach out to Cole @ hagencolej@gmail.com")
    
        
