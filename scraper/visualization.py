from junitparser import JUnitXml
import streamlit as st
import os
import pandas as pd

test_xml = JUnitXml.fromfile("/src/scraper/test_results.xml")

st.header("IMDB TOP 20 corrected ratings")

st.subheader("Test results")
st.write(f"Ran {test_xml.tests} tests.")
st.write(f"{test_xml.errors} failed")
st.write(f"{test_xml.tests - test_xml.errors} succeeded.")

top20_ratings_location = os.environ.get("OUTPUT_LOCATION")

raw_df = pd.read_csv(f"{top20_ratings_location}/top20_movies_corrected_ratings.csv")
df = raw_df.copy(deep=True)
df.drop("review_penalty", axis=1, inplace=True)
df.drop("oscar_bins", axis=1, inplace=True)
df.columns = ["Title", "Rating", "Number of votes", "Oscars won", "Corrected rating"]
df = df[["Title", "Oscars won", "Number of votes", "Rating", "Corrected rating"]]

st.subheader("TOP 20 movies with corrected ratings.")
st.dataframe(df)


@st.cache_data
def convert_df(df):
    return df.to_csv(index=False).encode("utf-8")


file_to_download = convert_df(raw_df)

st.download_button(
    "Press to Download the raw CSV file.",
    file_to_download,
    "imdb_top20_corrected_ratings.csv",
    "text/csv",
    key="download-csv",
)
