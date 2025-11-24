import time

import pandas as pd
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



# 7 pd.DataFrame ne akha dataframe ui vr disayala help kart

data = pd.DataFrame(
    {
        "name" : ["satish" , "shubham" , "sanket"],
        "marks" : [70,80,10]
    },

)
st.dataframe(data)

# 8 st.metric
st.metric('income','2L','5%')
st.metric('income','2L','-5%')

# 9 st.json backend kadun yenari jason file ui vr show krt.
st.json(
    {
        "name" : ["satish" , "shubham" , "sanket"],
        "marks" : [70,80,10]
    }
)

# 9 st.sidebar side la aik section yet menu type sarkh left side la.
st.sidebar.title("About")

# 10 st.progress ne aik bar banato jo loading sarkha asto te load zalya shivay khalach kahi load hot nahi.
bar = st.progress(0)
for i in range(100):
    time.sleep(0.01)
    bar.progress(i)


# 10 st.error mhanje ui vr aaplyala show krt kahi error asel tr red bar chya aat
#    st.success mhanje ui vr aaplyala show krt je success asel te green bar chya aat.
st.error("Error")
st.success("Success")

# 11 st.text_input hyane aik box create hoto jyacha aat pn lihu shakto
email = st.text_input("Email")
passw = st.text_input("Enter your password")

# 12 st.date_input ne aaplya ui vr calender yet jyatun aapan date select karu shakato.
st.date_input("Enter your date")

# 13 st.selectbox ne aik multi option box create hoto jya madhun aapan aik option select karu shakto.
st.selectbox('select',["Male","Female"])

# 14 st.button ne aik botton create
st.button("Click me")

# 15
btn = st.button("Login")
if btn:
    st.success("Login Successful")
    st.balloons()


