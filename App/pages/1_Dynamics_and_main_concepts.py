import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from config import PREPROCESSED_DIR, ASSETS_DIR

@st.cache_data
def amt_by_years():
    return pd.read_csv(PREPROCESSED_DIR / "amt_by_years.csv")
@st.cache_data
def medal_by_year():
    return pd.read_csv(PREPROCESSED_DIR / "medal_by_year.csv")
@st.cache_data
def medals_and_part():
    return pd.read_csv(PREPROCESSED_DIR / "medals_and_partc.csv")
@st.cache_data
def medal_comp():
    return pd.read_csv(PREPROCESSED_DIR / "df_medal_comp.csv")

st.title("Some History, overall dynamic and main concepts")

## amt_part
st.header("Participants")
st.subheader("Amount of participants (countries) by year")
b1, b2 = st.columns(2)
with b1:
    year_from = st.number_input("From: ", min_value=1896, max_value=2020, value=1900, step=1)
with b2:
    year_to = st.number_input("To: ", min_value=1900, max_value=2024, value=2020, step=1)
amt_by_years_df = amt_by_years()
amt_by_years_df = amt_by_years_df.loc[(amt_by_years_df["Year"] >= year_from) & (amt_by_years_df["Year"] <= year_to)]
st.dataframe(amt_by_years_df)
st.markdown("""#### Plot №1: Increasing number of participants
You may see NaN bars in 1910x | 1940x -> it is the consequences of Great Wars""")
fig, ax = plt.subplots()
ax.bar(height=amt_by_years_df["total_by_year"], x=amt_by_years_df["Year"], color="slateblue", edgecolor="darkblue")
st.pyplot(fig)
plt.close(fig)
cn1, cn2 = st.columns(2)
with cn1:
    st.write("Sex distribution -> ")
with cn2:
    st.page_link("pages/2_Sex_difference.py", label="See sex distribution")

## medals
st.header("Medals")
st.write("\n\nMedals Info")
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.image(ASSETS_DIR / "medals.png", width=280)
st.markdown("""Traditional system with three medals [Gold, Silver, Bronze] was established in **1904**, USA""")
medal_by_year_df = medal_by_year()
show_medals_df = st.checkbox("Show Data", value=True)
if show_medals_df:
    st.dataframe(medal_by_year_df)
years_range = st.slider("Select years range ", min_value=1896, max_value=2024, value=(1900, 2016), step=1)
medal_by_year_df = medal_by_year_df.loc[(medal_by_year_df["year"] >= years_range[0]) & (medal_by_year_df["year"] <= years_range[1])]
fig, ax = plt.subplots()
ax.plot(medal_by_year_df.loc[medal_by_year_df["medal"] == "Bronze", "year"],
         medal_by_year_df.loc[medal_by_year_df["medal"] == "Bronze", "total"], color="yellowgreen", label="Bronze")
ax.plot(medal_by_year_df.loc[medal_by_year_df["medal"] == "Silver", "year"],
         medal_by_year_df.loc[medal_by_year_df["medal"] == "Silver", "total"], color="grey", label="Silver")
ax.plot(medal_by_year_df.loc[medal_by_year_df["medal"] == "Gold", "year"],
         medal_by_year_df.loc[medal_by_year_df["medal"] == "Gold", "total"], color="orange", label="Gold")
plt.title("Medal dynamic")
plt.legend()
st.pyplot(fig)
plt.close(fig)

medals_and_part_df = medals_and_part()
medals_and_part_df = medals_and_part_df.loc[(medals_and_part_df["year"] >= years_range[0]) & (medals_and_part_df["year"] <= years_range[1])]
fig, ax = plt.subplots()
ax.stairs(medals_and_part_df["ratio%"], color="crimson", linewidth=1.75)
plt.title("Medals and participants ratio")
st.write("Ratio of participants and medals by year (e.g. 1n 1896: total_participants -> 182, total_medals -> 147, ratio -> 80%")
st.pyplot(fig)
plt.close(fig)

df_medal_comp = medal_comp()
df_medal_comp = df_medal_comp.loc[(df_medal_comp["year"] >= years_range[0]) & (df_medal_comp["year"] <= years_range[1])]
fig, ax = plt.subplots()
ax.bar(df_medal_comp["year"], df_medal_comp["total_medals_usa"], label="USA", color="mediumseagreen")
bars = ax.bar(df_medal_comp["year"], df_medal_comp["total_medals_other"],
              bottom=df_medal_comp["total_medals_usa"], label="Others", color="palevioletred")
ax.bar_label(bars, labels=[f"{p:.1f}%" for p in df_medal_comp["ratio%"]], padding=3)
plt.title("USA and others")
plt.legend()
st.write("Amount of USA medals in comparison to other countries")
st.pyplot(fig)
plt.close(fig)
st.write("1904 year is interesting: due to political conflicts a lot of countries hasn't arrive")
st.image(ASSETS_DIR / "rus_usa_medals.png", width=660)
st.markdown("USA, URS and Russia comparison")



## summer / winter games
st.header("Summer / Winter Games")
st.markdown("""Winter Games are held since **1924** (France)""")
st.subheader("""Summer games ratio: 78.24% / Winter games: 20.92% (1896-2022 ratio)""")
