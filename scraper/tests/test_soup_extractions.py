from bs4 import BeautifulSoup
from scraper import extract_ratings, extract_movie_titles, extract_movie_hrefs, extract_nr_of_votes

# I used ChatGPT to generate my test cases, only modified and appended some of them.
# If I had more time i would modularize the cases, but my chilren are jumping around me now

def test_extract_ratings_empty_soup():
    # Test with empty BeautifulSoup object
    soup = BeautifulSoup("", "html.parser")
    expected_output = []
    assert extract_ratings(soup) == expected_output

def test_extract_ratings_no_ratings():
    # Test with no ratings in the soup
    soup = BeautifulSoup("<html><body></body></html>", "html.parser")
    expected_output = []
    assert extract_ratings(soup) == expected_output

def test_extract_ratings_one_rating():
    # Test with only one rating in the soup
    soup = BeautifulSoup(
        "<html><body><table><tr><td class='posterColumn'><span name='ir' data-value='7.5'></span></td></tr></table></body></html>", "html.parser")
    expected_output = ['7.5']
    assert extract_ratings(soup) == expected_output

def test_extract_ratings_multiple_ratings():
    # Test with multiple ratings in the soup
    soup = BeautifulSoup(
        "<html><body><table><tr><td class='posterColumn'><span name='ir' data-value='7.5'></span></td></tr><tr><td class='posterColumn'><span name='ir' data-value='8.5'></span></td></tr><tr><td class='posterColumn'><span name='ir' data-value='6.5'></span></td></tr></table></body></html>", "html.parser")
    expected_output = ['7.5', '8.5', '6.5']
    assert extract_ratings(soup) == expected_output

def test_extract_movie_titles_empty_soup():
    # Test with empty BeautifulSoup object
    soup = BeautifulSoup("", "html.parser")
    expected_output = []
    assert extract_movie_titles(soup) == expected_output

def test_extract_movie_titles_no_movies():
    # Test with no movie titles in the soup
    soup = BeautifulSoup("<html><body></body></html>", "html.parser")
    expected_output = []
    assert extract_movie_titles(soup) == expected_output

def test_extract_movie_titles_one_movie():
    # Test with only one movie title in the soup
    soup = BeautifulSoup(
        """<html><body><table><tr><td class="titleColumn">
       1.
       <a href="/title/tt0111161/" title="Frank Darabont (dir.), Tim Robbins, Morgan Freeman">Shawshank redemption</a>
 <span class="secondaryInfo">(1994)</span>
 </td></tr></table></body></html>""", "html.parser")
    expected_output = ['Shawshank redemption']
    assert extract_movie_titles(soup) == expected_output

def test_extract_movie_titles_multiple_movies():
    # Test with multiple movie titles in the soup
    soup = BeautifulSoup(
        """<html><body><table><tr><td class="titleColumn">
       1.
       <a href="/title/tt0111161/" title="Frank Darabont (dir.), Tim Robbins, Morgan Freeman">Shawshank redemption</a>
        <span class="secondaryInfo">(1994)</span>
        </td></tr><tr>

        <tr><td class="titleColumn">
       2.
       <a href="/title/tt0111162/" title="Frank Darabont (dir.), Tim Robbins, Morgan Freeman">Inception</a>
        <span class="secondaryInfo">(1994)</span>
        </td></tr>
        </table></body></html>""", "html.parser")
    expected_output = ['Shawshank redemption', 'Inception']
    assert extract_movie_titles(soup) == expected_output

def test_extract_movie_hrefs_empty_soup():
    # Test with empty BeautifulSoup object
    soup = BeautifulSoup("", "html.parser")
    expected_output = []
    assert extract_movie_hrefs(soup) == expected_output

def test_extract_movie_hrefs_no_movies():
    # Test with no movie titles in the soup
    soup = BeautifulSoup("<html><body></body></html>", "html.parser")
    expected_output = []
    assert extract_movie_hrefs(soup) == expected_output

def test_extract_movie_hrefs_one_movie():
    # Test with only one movie title in the soup
    soup = BeautifulSoup(
        "<html><body><table><tr><td class='titleColumn'><a href='/title/tt1375666/' title='Inception (2010)'>Inception</a></td></tr></table></body></html>", "html.parser")
    expected_output = ['/title/tt1375666/']
    assert extract_movie_hrefs(soup) == expected_output

def test_extract_movie_hrefs_multiple_movies():
    # Test with multiple movie titles in the soup
    soup = BeautifulSoup(
        "<html><body><table><tr><td class='titleColumn'><a href='/title/tt1375666/' title='Inception (2010)'>Inception</a></td></tr><tr><td class='titleColumn'><a href='/title/tt0816692/' title='Interstellar (2014)'>Interstellar</a></td></tr><tr><td class='titleColumn'><a href='/title/tt0816711/' title='The Martian (2015)'>The Martian</a></td></tr></table></body></html>", "html.parser")
    expected_output = ['/title/tt1375666/', '/title/tt0816692/', '/title/tt0816711/']
    assert extract_movie_hrefs(soup) == expected_output

def test_extract_movie_hrefs_missing_a_tag():
    # Test with a td tag missing an a tag
    soup = BeautifulSoup(
        "<html><body><table><tr><td class='titleColumn'></td></tr></table></body></html>", "html.parser")
    expected_output = [None]
    assert extract_movie_hrefs(soup) == expected_output

def test_extract_movie_hrefs_multiple_missing_a_tags():
    # Test with multiple td tags missing an a tag
    soup = BeautifulSoup(
        "<html><body><table><tr><td class='titleColumn'></td></tr><tr><td class='titleColumn'></td></tr><tr><td class='titleColumn'><a href='/title/tt0076759/' title='Star Wars: Episode IV - A New Hope (1977)'>Star Wars: Episode IV - A New Hope</a></td></tr><tr><td class='titleColumn'></td></tr></table></body></html>", "html.parser")
    expected_output = [None, None, '/title/tt0076759/', None]
    assert extract_movie_hrefs(soup) == expected_output

def test_extract_nr_of_votes_empty_soup():
    # Test with empty BeautifulSoup object
    soup = BeautifulSoup("", "html.parser")
    expected_output = []
    assert extract_nr_of_votes(soup) == expected_output

def test_extract_nr_of_votes_no_ratings():
    # Test with no ratings in the soup
    soup = BeautifulSoup("<html><body></body></html>", "html.parser")
    expected_output = []
    assert extract_nr_of_votes(soup) == expected_output

def test_extract_nr_of_votes_one_movie():
    # Test with only one rating in the soup
    soup = BeautifulSoup(
        "<html><body><table><tr><td class='posterColumn'><span name='nv' data-value='500'></span></td></tr></table></body></html>", "html.parser")
    expected_output = [500]
    assert extract_nr_of_votes(soup) == expected_output

def test_extract_nr_of_votes_multiple_movies():
    # Test with multiple ratings in the soup
    soup = BeautifulSoup(
        """<html><body><table><tr><td class="titleColumn">
       1.
       <a href="/title/tt0111161/" title="Frank Darabont (dir.), Tim Robbins, Morgan Freeman">Shawshank redemption</a>
        <span class="secondaryInfo">(1994)</span>
        </td></tr>
        <td class=posterColumn><span data-value="500" name="nv"></span></td>
        <tr>

        <tr><td class="titleColumn">
       2.
       <a href="/title/tt0111162/" title="Frank Darabont (dir.), Tim Robbins, Morgan Freeman">Inception</a>
        <span class="secondaryInfo">(1994)</span>
        </td></tr>
        <td class=posterColumn><span data-value="600" name="nv"></span></td>
        </table></body></html>""", "html.parser")
    expected_output = [500, 600]
    assert extract_nr_of_votes(soup) == expected_output