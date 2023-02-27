from scraper import correct_movie_rating
import pandas as pd

def test_correct_rating():
    df = pd.DataFrame({
        "title": ["movie1", "movie2", "movie3"], 
        "rating": [8.0, 8.6, 9.7],
        "oscar_bins": [1.0, 0.0, 0.3],
        "review_penalty": [1.1, 2.0, 0.7]
        })
        
    result_df = correct_movie_rating(df)
    expected_corrected_rating = [9.3, 7.9, 6.6] # function sorts the order!
    assert result_df["corrected_rating"].tolist() == expected_corrected_rating