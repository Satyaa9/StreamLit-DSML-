import pandas as pd
import streamlit as st
import joblib
import plotly.express as px

st.set_page_config(page_title="Startup Funding Dashboard", layout="wide")

# ---------------- Load data ----------------
df = pd.read_csv("startup_cleaned.csv")

df["year"] = pd.to_datetime(df["date"]).dt.year
df["amount"] = pd.to_numeric(df["amount"], errors="coerce").fillna(0)

# Build clean investor list
inv_series = (
    df["investors"]
    .fillna("")
    .str.split(",")
    .explode()
    .str.strip()
)

investor_list = sorted(inv_series[inv_series != ""].unique())

# ---------------- Load model ----------------
try:
    model = joblib.load("funding_model.pkl")
except:
    model = None


# ---------------- Prediction UI ----------------
def show_prediction(df, model):
    st.markdown("<h1 style='color:#E91E63;'>🔮 Funding Prediction</h1>", unsafe_allow_html=True)

    if model is None:
        st.error("❌ Model file not found. Train the model first.")
        return

    verticals = sorted(df["vertical"].dropna().unique().tolist())
    cities = sorted(df["city"].dropna().unique().tolist())

    col1, col2 = st.columns(2)

    with col1:
        vertical = st.selectbox("📌 Sector / Vertical", verticals)
        city = st.selectbox("🏙 City", cities)

    with col2:
        year = st.slider("📅 Year", 2010, 2025, 2020)
        num_investors = st.slider("👨‍💼 Expected Investors", 1, 10, 2)

    if st.button("Predict Funding Amount 💰"):

        input_df = pd.DataFrame([{
            "vertical": vertical,
            "city": city,
            "year": year,
            "num_investors": num_investors,
            "sector_avg": df[df["vertical"] == vertical]["amount"].mean(),
            "city_avg": df[df["city"] == city]["amount"].mean(),
            "startup_total": df[df["vertical"] == vertical]["amount"].sum()
        }])

        predicted = model.predict(input_df)[0]
        usd_value = predicted / 83

        st.markdown(f"""
        <div style='padding:30px;border-radius:20px;background:#1e1e1e;color:white;text-align:center;
                    box-shadow:0 0 15px rgba(255,255,255,0.2);'>
            <h2 style='color:#00E676;'>✅ Realistic Funding Estimate</h2>
            <h1 style='font-size:48px;'>₹ {predicted:,.0f}</h1>
            <h3 style='font-size:32px;color:#03A9F4;'>≈ $ {usd_value:,.2f} USD</h3>
        </div>
        """, unsafe_allow_html=True)


# ---------------- Sidebar ----------------
st.sidebar.markdown("<h1 style='color:#FF9800;'>Startup Funding</h1>", unsafe_allow_html=True)

option = st.sidebar.selectbox(
    '📌 Select Section',
    ["Overall", "StartUp", "Investor", "Funding Prediction", "Investor Recommendation"]
)


# ---------------- MAIN UI ----------------
if option == "Overall":
    st.markdown("<h1 style='color:#2196F3;'>📊 Overall Funding Overview</h1>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Startups", df['startup'].nunique())
    col2.metric("Total Investors", len(investor_list))
    col3.metric("Total Funding ₹", f"{df['amount'].sum():,.0f}")

    st.write("---")
    st.subheader("📅 Latest Funding Deals")
    st.dataframe(df.head(10), use_container_width=True)



elif option == "StartUp":
    st.markdown("<h1 style='color:#9C27B0;'>🚀 Startup Details</h1>", unsafe_allow_html=True)

    startup = st.sidebar.selectbox("🔍 Select Startup", sorted(df["startup"].unique().tolist()))

    data = df[df["startup"] == startup]

    st.write(f"### 📌 {startup}")
    st.dataframe(data, use_container_width=True)



elif option == "Investor":
    st.markdown("<h1 style='color:#4CAF50;'>💼 Investor Analysis</h1>", unsafe_allow_html=True)

    investor = st.sidebar.selectbox('🏦 Select Investor', investor_list)

    investor_data = df[df["investors"].fillna("").str.contains(investor, regex=False)]

    st.subheader(f"📊 Year-wise Investment by {investor}")

    yearly = investor_data.groupby("year")["amount"].sum().reset_index()

    if not yearly.empty:
        fig = px.line(yearly, x="year", y="amount", markers=True,
                      title=f"Year-wise Investment by {investor}")
        st.plotly_chart(fig, use_container_width=True)

    # ✅ Sector Pie Chart
    st.subheader("🥧 Sector-wise Investment Share")
    sector_data = investor_data.groupby("vertical")["amount"].sum().reset_index()

    if not sector_data.empty:
        fig2 = px.pie(sector_data, names="vertical", values="amount")
        st.plotly_chart(fig2, use_container_width=True)

    # ✅ Top 5 startups
    st.subheader("🏆 Top 5 Startups Funded")

    top5 = (
        investor_data.groupby("startup")["amount"]
        .sum()
        .sort_values(ascending=False)
        .head(5)
    )

    if not top5.empty:
        st.bar_chart(top5)

    # ✅ Investor Comparison
    if st.sidebar.checkbox("Compare Investors"):
        inv2 = st.sidebar.selectbox("Select another investor", [i for i in investor_list if i != investor])

        inv1_amt = investor_data["amount"].sum()
        inv2_data = df[df["investors"].fillna("").str.contains(inv2, regex=False)]
        inv2_amt = inv2_data["amount"].sum()

        compare_df = pd.DataFrame({
            "Investor": [investor, inv2],
            "Investment": [inv1_amt, inv2_amt]
        })

        st.subheader("⚔️ Investment Comparison")
        st.bar_chart(compare_df.set_index("Investor"))

    # ✅ AI Insight
    st.subheader("🤖 AI Insight: Why this investor invested?")

    reason = ""

    if not sector_data.empty and sector_data["amount"].max() > sector_data["amount"].mean() * 2:
        top_sector = sector_data.sort_values("amount", ascending=False)["vertical"].iloc[0]
        reason += f"🔹 Strong focus on **{top_sector}** sector\n\n"

    if not yearly.empty and len(yearly) > 1:
        if yearly["amount"].iloc[-1] > yearly["amount"].iloc[0]:
            reason += "📈 Increasing investment trend\n\n"
        else:
            reason += "📉 Decreasing investment trend\n\n"

    if not top5.empty and top5.iloc[0] > top5.mean():
        top_startup = top5.index[0]
        reason += f"🚀 Major investment in **{top_startup}**\n\n"

    if reason == "":
        reason = "🤷 No strong investment pattern."

    st.write(reason)

    st.write("### 🧾 Investment Summary")
    st.dataframe(
        investor_data[["date", "startup", "vertical", "amount"]]
        .sort_values("date", ascending=False),
        use_container_width=True
    )



elif option == "Funding Prediction":
    show_prediction(df, model)



elif option == "Investor Recommendation":
    st.markdown("<h1 style='color:#FF4081;'>🤖 Investor Recommendation AI</h1>", unsafe_allow_html=True)

    startup = st.sidebar.selectbox("🔍 Select Startup", sorted(df["startup"].unique().tolist()))

    data = df[df["startup"] == startup]

    if data.empty:
        st.error("No data available.")
    else:
        sector = data["vertical"].iloc[0]
        city = data["city"].iloc[0]

        st.write(f"📌 Sector: **{sector}**")
        st.write(f"📍 City: **{city}**")

        investor_scores = {}

        for inv in investor_list:
            rows = df[df["investors"].fillna("").str.contains(inv, regex=False)]

            if rows.empty:
                continue

            score = 0
            if sector in rows["vertical"].values:
                score += 3
            if city in rows["city"].values:
                score += 2
            score += rows["amount"].sum() / 1e7
            score += rows["year"].max() / 2025

            investor_scores[inv] = score

        rec = sorted(investor_scores.items(), key=lambda x: x[1], reverse=True)[:5]

        st.subheader("🏆 Best Investor Matches")

        for inv, sc in rec:
            st.markdown(f"✅ **{inv}** — Score: {sc:.2f}")

        st.subheader("🧠 Why these investors?")

        top_inv = rec[0][0]
        top_rows = df[df["investors"].fillna("").str.contains(top_inv, regex=False)]

        insight = ""

        if sector in top_rows["vertical"].values:
            insight += f"🔹 Strong in **{sector}** sector\n\n"

        if city in top_rows["city"].values:
            insight += f"📍 Active in **{city}**\n\n"

        if top_rows["amount"].sum() > df["amount"].mean():
            insight += "💰 Large deal history\n\n"

        if top_rows["year"].max() >= df["year"].quantile(0.75):
            insight += "📈 Recently active\n\n"

        if insight == "":
            insight = "🤷 No strong pattern."

        st.write(insight)
