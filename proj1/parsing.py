"""Method for parsing HTML pages and tokenizing text."""
import bs4

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

def tokenize_text(text):
    # TODO(kevin): consider more intelligent term lexing here
    return [x.lower() for x in text.split()]
