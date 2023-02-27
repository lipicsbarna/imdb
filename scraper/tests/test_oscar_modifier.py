from scraper import bin_oscars, add_oscar_modifier_to_df
import pandas as pd
import pytest

@pytest.mark.parametrize("nr_of_oscars, expected", [
    (-1, ValueError),
    (2.5, TypeError),
    ("five", TypeError),
    (0, 0),
    (1, 0.3),
    (2, 0.3),
    (3, 0.5),
    (4, 0.5),
    (5, 0.5),
    (6, 1),
    (7, 1),
    (10, 1),
    (11, 1.5),
])
def test_bin_oscars(nr_of_oscars, expected):
    if expected == ValueError:
        with pytest.raises(ValueError):
            bin_oscars(nr_of_oscars)
    elif expected == TypeError:
        with pytest.raises(TypeError):
            bin_oscars(nr_of_oscars)
    else:
        assert bin_oscars(nr_of_oscars) == expected

def test_add_oscar_modifier_to_df_output_validation():
    df = pd.DataFrame({"title": ["movie1", "movie2", "movie3"], "nr_of_oscars": [0, 5, 11]})
    expected_df = pd.DataFrame({"title": ["movie1", "movie2", "movie3"], "nr_of_oscars": [0, 5, 11], "oscar_bins": [0, 0.5, 1.5]})
    
    result_df = add_oscar_modifier_to_df(df)
    assert result_df["oscar_bins"].tolist() == expected_df["oscar_bins"].tolist()