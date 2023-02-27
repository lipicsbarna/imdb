from scraper import calculate_review_penalty
import pandas as pd
from numpy.testing import assert_almost_equal

def test_calculate_review_penalty():
    df = pd.DataFrame({
        "nr_of_votes": [1008369, 1258369, 2456123]
    })
    expected_df = pd.DataFrame({
        "nr_of_votes": [1008369, 1258369, 2456123],
        "review_penalty": [1.4, 1.1, 0.0]
    })
    result_df = calculate_review_penalty(df)
    #sassert_almost_equal(result_df.values, expected_df.values, decimal=2)
    pd.testing.assert_frame_equal(result_df, expected_df)