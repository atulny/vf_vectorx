import sys

import streamlit as st
sys.path.append(".")
from clerkjs import clerkjs


st.subheader("User Login")

data = clerkjs("World")
if data:
    print("session_data")
    print(data)
