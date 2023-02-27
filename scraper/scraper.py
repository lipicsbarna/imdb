from bs4 import BeautifulSoup
from bs4.element import Tag
import requests
import re
import pandas as pd
import urllib3
import logging
import sys
from dataclasses import dataclass
from math import floor
import os

OUTPUT_LOCATION = os.environ.get("OUTPUT_LOCATION")
if OUTPUT_LOCATION is None:
    raise ValueError("Could not resolve file output location from env variables.")

urllib3.disable_warnings()

URL = "https://www.imdb.com/chart/top"
TOP_NR_TO_TAKE = 20

# If we had more data I would optimise the iteration algorithm
def extract_movie_title(movie: Tag) -> str:
    try:
        return movie.get_text().split("\n")[2].strip()
    except (AttributeError, IndexError):
        return None


def extract_movie_titles(soup: BeautifulSoup) -> list[str]:

    return [extract_movie_title(movie) for movie in soup.select("td.titleColumn")]


def extract_movie_hrefs(soup: BeautifulSoup) -> list[str]:
    movie_hrefs = []
    for tag in soup.select("td.titleColumn"):
        a_tags = tag.findChildren("a")
        if a_tags:
            hrefs = a_tags[0].get_attribute_list("href")
            movie_hrefs.extend(hrefs)
        else:
            movie_hrefs.append(None)
    return movie_hrefs


def extract_ratings(soup: BeautifulSoup) -> list[float]:

    _ratings = [
        rating.attrs.get("data-value")
        for rating in soup.select("td.posterColumn span[name=ir]")
    ]

    return _ratings


def extract_nr_of_votes(soup: BeautifulSoup) -> list[int]:

    nr_of_votes = [
        int(nr_of_vote.attrs.get("data-value"))
        for nr_of_vote in soup.select("td.posterColumn span[name=nv]")
    ]

    return nr_of_votes


def extract_nr_of_oscars(movie_url: str, logger: logging.Logger) -> int:
    result = requests.get(
        movie_url, verify=False, headers={"User-Agent": "Mozilla/5.0"}
    )
    content = result.text
    soup = BeautifulSoup(content, "lxml")
    element = soup.find_all(class_="ipc-metadata-list-item__label")

    try:
        extracted_text = element[6].get_text(strip=True).split()
        if extracted_text[0] == "Won" and "Oscar" in extracted_text[-1]:
            nr_of_oscars = int(extracted_text[1])
        else:
            nr_of_oscars = 0
    except IndexError:
        nr_of_oscars = 0

    logger.debug(f"Number of oscars extracted for url: {movie_url}")
    return nr_of_oscars


def validate_movie_params(
    top_nr_to_take: int,
    movie_titles: list[str],
    ratings: list[float],
    nr_of_votes: list[int],
    nr_of_oscars: list[int],
    logger: logging.Logger,
):

    for prop_name, prop in {
        "movie_titles": movie_titles,
        "ratings": ratings,
        "nr_of_votes": nr_of_votes,
        "nr_of_oscars": nr_of_oscars,
    }.items():
        try:
            assert len(prop) == top_nr_to_take
        except AssertionError:
            logger.error(
                f"""Number of elements in {prop_name} is not matching the configured {top_nr_to_take}. 
                         The length of it is {len(prop)}"""
            )
            raise


def df_from_movie_info(
    movie_titles: list[str],
    ratings: list[float],
    nr_of_votes: list[int],
    nr_of_oscars: list[int],
    top_nr_to_take: int,
    logger: logging.Logger,
):
    df = pd.DataFrame(
        zip(movie_titles, ratings, nr_of_votes, nr_of_oscars),
        columns=["title", "rating", "nr_of_votes", "nr_of_oscars"],
    )

    expected_types = {"rating": float, "nr_of_votes": int, "nr_of_oscars": int}
    for column, _type in expected_types.items():
        try:
            df[column] = df[column].astype(_type)
            assert len(df) == top_nr_to_take
        except AssertionError:
            logger.error(f"Some rows had mismatched value types in column {column}")
            raise
        except:
            logger.error(f"Type validation failed for column: {column}")
            raise

    return df


def calculate_review_penalty(df: pd.DataFrame) -> pd.DataFrame:
    max_votes = df["nr_of_votes"].max()

    df["review_penalty"] = df["nr_of_votes"].apply(
        lambda x: round(floor((max_votes - x) / 100000) * 0.1, 1)
    )
    return df


def bin_oscars(nr_of_oscars: int):
    if nr_of_oscars < 0:
        raise ValueError(f"Nr of oscars is negative: {nr_of_oscars}")
    elif not isinstance(nr_of_oscars, int):
        raise TypeError("Type mismatch, nr_of_oscars should be integer.")
    elif nr_of_oscars == 0:
        return 0
    elif nr_of_oscars in {1, 2}:
        return 0.3
    elif nr_of_oscars >= 3 and nr_of_oscars <= 5:
        return 0.5
    elif nr_of_oscars >= 6 and nr_of_oscars <= 10:
        return 1
    else:
        return 1.5


def add_oscar_modifier_to_df(df: pd.DataFrame):

    df["oscar_bins"] = df["nr_of_oscars"].apply(lambda x: bin_oscars(x))
    return df


def correct_movie_rating(df: pd.DataFrame):

    df["corrected_rating"] = df["rating"] - df["review_penalty"] + df["oscar_bins"]
    return df.sort_values("corrected_rating", ascending=False)


if __name__ == "__main__":
    logging.basicConfig(
        format="%(asctime)s %(name)s:%(levelname)s %(message)s",
        level=logging.INFO,
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    logger = logging.getLogger("imdbscraper")

    try:
        response = requests.get(URL, verify=False)
        soup = BeautifulSoup(response.text, "html.parser")
        logger.info("IMDB page loaded to scraper")
    except:
        logger.error("Error at loading IMDB page to scraper")
        raise

    try:
        movie_titles: list[str] = extract_movie_titles(soup)[0:TOP_NR_TO_TAKE]
        logger.info("Movie titles are extracted.")

        ratings: list[float] = extract_ratings(soup)[0:TOP_NR_TO_TAKE]
        logger.info("Movie ratings are extracted.")

        nr_of_votes: list[int] = extract_nr_of_votes(soup)[0:TOP_NR_TO_TAKE]
        logger.info("Number of votes are extracted.")

        movie_hrefs: list[str] = extract_movie_hrefs(soup)[0:TOP_NR_TO_TAKE]
        logger.info("Movie urls are extracted.")
        nr_of_oscars = [
            extract_nr_of_oscars(movie_url=f"https://www.imdb.com{url}", logger=logger)
            for url in movie_hrefs
        ]
        logger.info("Number of oscars are extracted")
    except:
        logger.error("Failed to extract movie info.")
        raise

    validate_movie_params(
        top_nr_to_take=TOP_NR_TO_TAKE,
        movie_titles=movie_titles,
        ratings=ratings,
        nr_of_votes=nr_of_votes,
        nr_of_oscars=nr_of_oscars,
        logger=logger,
    )
    logging.info("Validating is OK.")

    try:
        df: pd.DataFrame = df_from_movie_info(
            movie_titles, ratings, nr_of_votes, nr_of_oscars, TOP_NR_TO_TAKE, logger
        )
    except:
        logger.error("Failed to generate dataframe from movie attributes.")
        raise

    try:
        df_with_review_penalties: pd.DataFrame = calculate_review_penalty(df)
        df_with_penalties_and_oscar_modifiers: pd.DataFrame = add_oscar_modifier_to_df(
            df_with_review_penalties
        )
        df_corrected_ratings: pd.DataFrame = correct_movie_rating(
            df_with_penalties_and_oscar_modifiers
        )
        logger.info("Corrected ratings are calculated.")

    except:
        logger.error("Generating corrected ratings failed.")
        raise

    try:
        df_corrected_ratings.to_csv(
            f"{OUTPUT_LOCATION}/top20_movies_corrected_ratings.csv", index=False
        )
        logger.info(f"Successfully written data to location: {OUTPUT_LOCATION}")
    except:
        logger.error(f"Failed to write end results to location: {OUTPUT_LOCATION}")
        raise
