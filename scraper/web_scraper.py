from typing import Tuple

import requests
import unicodedata
from bs4 import BeautifulSoup


def get_article(url: str) -> Tuple[str, str]:
    """
    Scrape the title and content from the given daily mail url

    Perform the following steps:
    1. Get the html code from the url.
    2. Parse the html code.
    3. Return the title and content.

    Args:
        url:

    Returns: A tuple of (title, content)

    """
    # get the html code
    page = requests.get(url)

    # parse the html code
    soup = BeautifulSoup(page.content, "html.parser")
    results = soup.find(id="js-article-text")

    # get title
    title = results.find("h2")
    title_text = title.get_text(strip=True)

    # get content
    article_body = results.find("div", itemprop="articleBody")
    article_para = article_body.find_all(
        "p", class_="mol-para-with-font", recursive=False
    )

    #  set strip=True to strip whitespace from the beginning and end of each bit of text
    para_list = [para.get_text(strip=True) for para in article_para]
    content = " ".join(para_list)
    # remove \xao
    cleaned_content = unicodedata.normalize("NFKD", content)

    return title_text, cleaned_content
