from scraper import calculate_review_penalty
import pandas as pd
from numpy.testing import assert_almost_equal

def test_calculate_review_penalty():
    df = pd.DataFrame({
        "nr_of_votes": [497647, 1000000, 1500000]
    })
    expected_df = pd.DataFrame({
        "nr_of_votes": [497647, 1000000, 1500000],
        "review_penalty": [1.0, 0.5, 0.0]
    })
    result_df = calculate_review_penalty(df)
    assert_almost_equal(result_df.values, expected_df.values, decimal=2)