import streamlit as st
import os

dirname = os.path.dirname(os.path.abspath(__file__))

def global_page_style2():  
    st.set_page_config(layout="wide")  
    with open(dirname + '/style.css') as f:
        css = f.read()
    st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)