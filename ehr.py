import streamlit as st
import pandas as pd
import plotly.express as px
import itertools
import numpy as np
from pycaret.regression import setup, create_model, finalize_model, predict_model
from streamlit.components.v1 import html
from deta import Deta

    

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

deta = Deta("b02l5gt3_MFtTQuHFmWUEofyrn54FjjnWxAevcaY1")
db = deta.Base("fitusers")

login_btn = st.button("Log In")
if login_btn:
    result = db.fetch().items
    df = pd.DataFrame(result)
    st.dataframe(df)
    user_check_df = df[df['user_name'] == user_name]
    try:
        if user_check_df['password'].iloc[-1] == password:
            db.put({"user_name": user_name, "password": password})
            nav_page("display")
        else:
            st.error("Incorrect password or user name. Please try again.")
    except:
        st.error("Incorrect password or user name. Please try again.")
account_btn = st.button("Create Account")
if account_btn:
    result1 = db.fetch().items
    df1 = pd.DataFrame(result1)
    user_check_df1 = df1[df1['user_name'] == user_name]
    if len(user_check_df1) < 1:
        
        db.put({"user_name": user_name, "password": password})
        st.info("Welcome " + user_name + " please proceed to login in with your new acount.")
    else:
        st.error("User Name Taken. If you already have an account, please enter your user name and select log in. If you are a new user, please enter a new user name.")
forgot_password = st.button("Change Password")
if forgot_password:
    st.info("Please reach out to Cole @ hagencolej@gmail.com")
    
        
