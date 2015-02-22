"""Method for parsing HTML pages and tokenizing text."""
import os
import re

import bs4
import nltk

nltk.data.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)),
                      'nltk_data'))

def extract_page_text(html):
    """Extracts the useful text from an HTML page.

    Args:
      html: a string of HTML contents from the page
    Returns:
      A string containing text with most of the HTML, JS, CSS, etc. stripped away
    """
    soup = bs4.BeautifulSoup(html)

    # Remove <script/> and <style/> content
    for script in soup(["script", "style"]):
        script.extract()

    text = soup.get_text()

    # Strip leading and trailing whitespace from each line, then join all the
    # non-empty lines together.
    lines = (line.strip() for line in text.splitlines())
    text = '\n'.join(line for line in lines if line)

    return text


_STOP_WORDS = nltk.corpus.stopwords.words('english')

def filter_tokens(x):
    """Filter to remove undesirable tokens from the list.

    Args:
      x: a string of the token
    Returns:
      True if the token is desirable and false if it is undesirable.
    """
    if x in _STOP_WORDS:
        return False
    if not re.search(r'\w', x):
        # Does not contain at least one word character
        return False
    return True

def tokenize_text(text):
    return [x for x in nltk.word_tokenize(text.lower()) if filter_tokens(x)]
