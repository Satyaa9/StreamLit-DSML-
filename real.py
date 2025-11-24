import pandas as pd
import streamlit as st

st.set_page_config(page_title="Startup Funding Dashboard", layout="wide")


df = pd.read_csv("startup_cleaned.csv")



def investor_details(investor):
    st.markdown(f"<h2 style='color:#4CAF50;'>Investor: {investor}</h2>", unsafe_allow_html=True)

    data = df[df["investors"].str.contains(investor)]
    data = data[["date", "startup", "vertical", "amount"]]

    st.dataframe(data, use_container_width=True)



st.sidebar.markdown("<h1 style='color:#FF9800;'>Startup Funding</h1>", unsafe_allow_html=True)

option = st.sidebar.selectbox('📌 Select Section', ["Overall", "StartUp", "Investor"])


if option == "Overall":
    st.markdown("<h1 style='color:#2196F3;'>📊 Overall Funding Overview</h1>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
            <div style='padding:20px;border-radius:15px;background:black;color:white;text-align:center;'>
                <h3>Total Startups</h3>
                <h2>{}</h2>
            </div>
        """.format(df['startup'].nunique()), unsafe_allow_html=True)

    with col2:
        st.markdown("""
            <div style='padding:20px;border-radius:15px;background:black;color:white;text-align:center;'>
                <h3>Total Investors</h3>
                <h2>{}</h2>
            </div>
        """.format(df['investors'].nunique()), unsafe_allow_html=True)

    with col3:
        st.markdown("""
            <div style='padding:20px;border-radius:15px;background:black;color:white;text-align:center;'>
                <h3>Total Funding Amount</h3>
                <h2>{:,.0f}</h2>
            </div>
        """.format(df['amount'].sum()), unsafe_allow_html=True)

    st.write("---")
    st.subheader("📅 Latest Funding Deals")
    st.dataframe(df.head(10), use_container_width=True)



elif option == "StartUp":
    st.markdown("<h1 style='color:#9C27B0;'>🚀 Startup Details</h1>", unsafe_allow_html=True)

    startup = st.sidebar.selectbox("🔍 Select Startup", sorted(df["startup"].unique().tolist()))

    data = df[df["startup"] == startup]

    try:
        vertical = data["vertical"].iloc[0]
        city = data["city"].iloc[0]
        investors = data["investors"].iloc[0]
    except:
        st.error("Some column names do not exist. Please check CSV.")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("<div style='padding:20px;border-radius:15px;background:black;color:white;text-align:center;'>"
                    "<h3>📌 Vertical</h3>"
                    f"<h2>{vertical}</h2>"
                    "</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("""
            <div style='padding:20px;border-radius:15px;background:black;color:white;text-align:center;'>
                <h3>🏢 City</h3>
                <h2>{}</h2>
            </div>
        """.format(city), unsafe_allow_html=True)

    st.markdown("""
        <div style='margin-top:25px;padding:20px;border-radius:15px;background:black;color:white;text-align:center;'>
            <h3>👨‍💼 Investors</h3>
            <h4>{}</h4>
        </div>
    """.format(investors), unsafe_allow_html=True)

    st.write("---")
    st.subheader("📜 Full Startup Record")
    st.dataframe(data, use_container_width=True)



else:
    st.markdown("<h1 style='color:#4CAF50;'>💼 Investor Analysis</h1>", unsafe_allow_html=True)

    investor_list = sorted(set(df["investors"].str.split(',').sum()))

    investor = st.sidebar.selectbox('🏦 Select Investor', investor_list)

    investor_details(investor)
