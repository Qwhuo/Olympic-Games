import streamlit as st
import joblib
import pandas as pd

from config import MODEL_PATH

@st.cache_resource
def load_model():
    return joblib.load(MODEL_PATH)

mod = load_model()

st.title("Predict amount of medals by country")
year = st.number_input("Year of participation ", min_value=800, max_value=2500, value=2028)
type = st.selectbox("Season ", ["Summer", "Winter"])
noc = st.text_input("NOC Code ", "USA", max_chars=5)
gdp = st.number_input("GDP ", min_value=0.0)
popul = st.number_input("Population ", min_value=0.0)
disciplines = st.slider("Amount of disciplines ", min_value=1, max_value=250, value=30)
athletes = st.slider("Amount of athlets ", min_value=1, max_value=15000, value=3500)
countries = st.slider("Amount of countries ", min_value=1, max_value=210, value=180)
events = st.slider("Amount of events ", min_value=1, max_value=500, value=250)
is_host = st.checkbox("Is host? ", value=False)

if st.button("< Predict >"):
    df = pd.DataFrame([{
        "year": year,
        "type": type,
        "noc": noc,
        "GPD": gdp,
        "Popul": popul,
        "Disciplines": disciplines,
        "Athletes": athletes,
        "total_countries": countries,
        "Events": events,
        "is_host": int(is_host),
    }])
    pred = mod.predict(df)[0]
    st.metric(
        "Predicted medals",
        max(0, round(pred)),
    )
