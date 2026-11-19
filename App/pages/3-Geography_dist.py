import streamlit as st
import pandas as pd
import plotly.express as px

from config import PREPROCESSED_DIR, ASSETS_DIR

@st.cache_data
def geography_dist():
    return pd.read_csv(PREPROCESSED_DIR / "countries_and_medals.csv")


st.title("Geography Distribution")

st.subheader("Host cities")
st.image(ASSETS_DIR / "hosts.png")

st.subheader("Cities and amount of medals")
countries_and_medals_df = geography_dist()
fig = px.choropleth(
    countries_and_medals_df,
    locations="Country Code",
    color="total_medals",
    hover_name="Country Name",
    color_continuous_scale="Viridis",
    projection="natural earth",
    title="Medals by Country",
    width=1400,
    height=800
)
st.plotly_chart(fig, use_container_width=True)
st.markdown("""*Note:* Amount of Russia's (and some other countries) medals is reduces, because of issues with old / new names""")
cn1, cn2 = st.columns(2)
with cn1:
    st.write("More about medals -> ")
with cn2:
    st.page_link("pages/1_Dynamics_and_main_concepts.py", label="See details")
