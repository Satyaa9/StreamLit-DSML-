import streamlit as st


# Methods of streamlit

# 1
st.title("Streamlit Lit")

# 2
st.header("Satish")

# 3
st.subheader("Dadas")

# 4 .markdown used to create a list
st.markdown("""
    # my data
    -shubham \n
    -sanket
    
""")

# 5 .code is used to write a code on our frontend.
st.code("""
    import pandas as pd
    def fun():
        print("in fun")
    fun()
""")

# 6 .latex is used to create a mathematical expression on our ui

st.latex('X^2 + Y^2 = 4')

