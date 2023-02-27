import logging
import pandas as pd
import pytest

from scraper import df_from_movie_info

@pytest.fixture
def logger():
    return logging.getLogger()

def test_df_from_movie_info_with_valid_data(logger):
    movie_titles = ["The Shawshank Redemption", "The Godfather", "The Dark Knight"]
    ratings = [9.2, 9.1, 9.0]
    nr_of_votes = [2446404, 1689228, 2428097]
    nr_of_oscars = [0, 3, 2]
    top_nr_to_take = 3
    
    df = df_from_movie_info(
        movie_titles, 
        ratings, 
        nr_of_votes, 
        nr_of_oscars, 
        top_nr_to_take, 
        logger
    )

    assert len(df) == top_nr_to_take
    assert df["rating"].dtype == float
    assert df["nr_of_votes"].dtype == int
    assert df["nr_of_oscars"].dtype == int
    assert set(df.columns) == {"title", "rating", "nr_of_votes", "nr_of_oscars"}
    assert df["title"].to_list() == movie_titles
    assert df["rating"].to_list() == ratings
    assert df["nr_of_votes"].to_list() == nr_of_votes
    assert df["nr_of_oscars"].to_list() == nr_of_oscars
    
def test_df_from_movie_info_with_mismatched_data_type(logger):
    movie_titles = ["The Shawshank Redemption", "The Godfather", "The Dark Knight"]
    ratings = ["Godfather", 9.1, 9.0]
    nr_of_votes = [12642324, 1689228, 2428097]  # mismatched data type
    nr_of_oscars = [0, 3, 2]
    top_nr_to_take = 3
    
    with pytest.raises(ValueError):
        df_from_movie_info(
            movie_titles, 
            ratings, 
            nr_of_votes, 
            nr_of_oscars, 
            top_nr_to_take, 
            logger
        )