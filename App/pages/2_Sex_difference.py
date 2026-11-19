import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

from config import PREPROCESSED_DIR, ASSETS_DIR
from sports_list import get_sports
sports = get_sports()

@st.cache_data
def part_by_year():
    return pd.read_csv(PREPROCESSED_DIR / "part_by_year.csv")
@st.cache_data
def sports_by_sex():
    return pd.read_csv(PREPROCESSED_DIR / "sports_by_sex.csv")
@st.cache_data
def medals_by_sex():
    return pd.read_csv(PREPROCESSED_DIR / "medals_by_sex.csv")

st.title("Females & Males Comparison")
st.write("\n")
st.markdown("""*Note:* women are allowed to participate in Olympic Games since 1900, however, they may officially choose any kind of sport they wish only since **XXI**
(women's boxing was included in the program for the first time in London, 2012)""")

##
part_by_year_df = part_by_year()
show_df = st.checkbox("Show Data", value=True)
if show_df:
    st.dataframe(part_by_year_df)
part_by_year_df["F"] = part_by_year_df["total_people"].where(part_by_year_df["Sex"] == "F")
part_by_year_df["M"] = part_by_year_df["total_people"].where(part_by_year_df["Sex"] == "M")
part_by_year_df["F"] = part_by_year_df["F"].fillna(0)
part_by_year_df["M"] = part_by_year_df["M"].fillna(0)
p_by_year = part_by_year_df.groupby("Year", as_index=False).agg(F_amt=("F", "max"), M_amt=("M", "max"))
part_by_year_df.to_csv("Data/preprocessed/part_by_year.csv", index=False)
opt1, opt2 = st.columns(2)
with opt1:
    show_man = st.checkbox("Show Man", value=True)
with opt2:
    show_woman = st.checkbox("Show Woman", value=True)
if not show_man and not show_woman:
    st.write("One option must be selected")
    show_woman = True
fig, ax = plt.subplots()
if show_woman:
    ax.bar(height=p_by_year["F_amt"],  x=p_by_year["Year"], label="Females", color="darkorange")
if show_man and show_woman:
    ax.bar(height=p_by_year["M_amt"],  x=p_by_year["Year"], label="Males", bottom=p_by_year["F_amt"], color="steelblue")
if show_man and not show_woman:
    ax.bar(height=p_by_year["M_amt"], x=p_by_year["Year"], label="Males", color="steelblue")
plt.legend()
st.pyplot(fig)
plt.close(fig)
st.write("Parity in amount of participants of different sexes will be achieved only by 2024\n\n\n")

##
st.subheader("Kinds of sport and women/men comparison")
sports_by_sex_df = sports_by_sex()
ind = 0
fig, axes = plt.subplots(nrows=10, ncols=6, figsize=(12, 10))
for i in range(10):
    for q in range(6):
        data = sports_by_sex_df.loc[sports_by_sex_df["Sport"] == sports[ind]]
        axes[i, q].plot(data.loc[data["Sex"] == "M", "Year"], data.loc[data["Sex"] == "M", "total"], color="steelblue")
        axes[i, q].plot(data.loc[data["Sex"] == "F", "Year"], data.loc[data["Sex"] == "F", "total"], color="purple")
        axes[i, q].set_title(sports[ind])
        ind += 1
st.pyplot(fig)
plt.close(fig)

##
st.subheader("Difference and standartised difference")
medals_by_sex_df = medals_by_sex()
styled_df = medals_by_sex_df.style.set_properties(**{
    "background-color": "#55634f",
    "color": "#FFF1D8",
    "border-color": "#749966"
})
st.dataframe(styled_df)
cn1, cn2 = st.columns(2)
with cn1:
    st.write("Medals Info -> ")
with cn2:
    st.page_link("pages/1_Dynamics_and_main_concepts.py", label="See medals details")

st.write("\nPie Chart repr")
fig2 = px.sunburst(medals_by_sex_df, path=["Sex", "Medal"], values="std", color="Medal")
st.plotly_chart(fig2, use_container_width=True)



col1, col2 = st.columns(2)
with col1:
    st.image(ASSETS_DIR / "figure_skating.png")
with col2:
    st.image(ASSETS_DIR / "figure_skating2.png")



