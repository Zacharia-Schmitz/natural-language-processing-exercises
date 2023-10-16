import pandas as pd
import requests
from bs4 import BeautifulSoup
import random


def random_header():
    """
    The function returns a randomly selected user agent header for web scraping purposes.
    :return: a dictionary with a single key-value pair, where the key is 'User-Agent' and the value is a
    randomly chosen user agent string from a list of user agents.
    """
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; rv:91.0) Gecko/20100101 Firefox/91.0",
        "Mozilla/5.0 (Windows NT 10.0; rv:78.0) Gecko/20100101 Firefox/78.0",
        "Mozilla/5.0 (X11; Linux x86_64; rv:95.0) Gecko/20100101 Firefox/95.0",
        "Chrome/91.0.4472.124",
        "Mozilla/4.5 (compatible; HTTrack 3.0x; Windows 98)",
    ]
    random_user_agent = random.choice(user_agents)
    return {"User-Agent": f"{random_user_agent}"}


def get_blog_articles(blogs_list=None, from_cache=False):
    """
    This function retrieves Codeup blog articles either from a cached CSV file or by scraping the
    website, and returns a pandas DataFrame containing the article titles and content.

    :param blogs_list: A list of URLs for Codeup blog articles. If not provided, the function will
    scrape the Codeup blog page to generate this list.
    :param from_cache: A boolean parameter that determines whether to read the data from a cached CSV
    file or to scrape the data from the website. Defaults to False.
    :return: A pandas DataFrame containing the title and content of blog articles from the Codeup
    website. If `from_cache` is set to `True`, it returns the cached DataFrame from a CSV file. If
    `from_cache` is `False` or there is no cached data, it scrapes the website for the blog articles
    and returns a new DataFrame.
    """
    # Define the filename for the cached CSV file
    filename = "codeup_blogs.csv"

    url = "https://codeup.edu/blog/"

    # If from_cache is True, read the data from the cached CSV file
    if from_cache:
        try:
            return pd.read_csv(filename)
        except FileNotFoundError:
            print(f"No cached data found in {filename}. Scraping website for data...")

    # If blogs_list is not provided, scrape the Codeup blog page to generate the list of URLs
    if blogs_list is None:
        # Make a request to the Codeup blog page and parse the HTML content using Beautiful Soup
        blog_page = requests.get("https://codeup.com/blog/", headers=random_header())
        blog_soup = BeautifulSoup(blog_page.content, "html.parser")

        # Find all the links to blog articles on the page and extract the URLs
        blogs_list = [element["href"] for element in blog_soup.select("a.more-link")]

    # Create an empty list to store the blog articles
    blogs = []

    # Loop through each URL in the blogs_list and scrape the article content
    for url in blogs_list:
        # Make a request to the blog article page and parse the HTML content using Beautiful Soup
        response = requests.get(url, headers=random_header())
        soup = BeautifulSoup(response.content, "html.parser")

        # Find the div containing the article content and extract the text of all the paragraphs
        content_div = soup.find("div", class_="entry-content")
        content = "".join(p.text for p in content_div.find_all("p"))

        # Create a dictionary containing the title and content of the blog article
        blog = {"title": soup.title.text, "content": content}

        # Append the blog dictionary to the list of blogs
        blogs.append(blog)

    # Create a pandas DataFrame from the list of blogs
    blogs_df = pd.DataFrame(blogs)

    # Cache the data locally by writing it to a CSV file
    blogs_df.to_csv("csv_files/" + filename, index=False)

    # Return the pandas DataFrame containing the blog article titles and content
    return blogs_df


def get_news_shorts(categories=None, from_cache=False, filename="news_shorts.csv"):
    """
    This function scrapes news shorts from the specified categories on the given website and returns a pandas DataFrame
    containing the title, content, and category of each news short.

    :param categories: A list of categories to scrape news shorts from. If not provided, the function will
    scrape news shorts from the default categories.
    :param from_cache: A boolean parameter that determines whether to read the data from a cached CSV
    file or to scrape the data from the website. Defaults to False.
    :param filename: The name of the CSV file to use for caching the data. Defaults to 'news_shorts.csv'.
    :return: A pandas DataFrame containing the title, content, and category of each news short.
    """
    # Define the base URL for the news shorts website
    url = "https://inshorts.com/en/read/"

    # Define the default categories to scrape news shorts from
    default_categories = ["business", "sports", "technology", "entertainment"]

    # If categories is not provided, use the default categories
    if categories is None:
        categories = default_categories

    # If from_cache is True, read the data from the cached CSV file
    if from_cache:
        try:
            return pd.read_csv(filename)
        except FileNotFoundError:
            print(f"No cached data found in {filename}. Scraping website for data...")

    # Create an empty list to store the news shorts
    shorts = []

    # Loop through each category
    for cat in categories:
        # Make a request to the webpage for the current category and parse the HTML content using Beautiful Soup
        response = requests.get(url + cat, headers=random_header())
        soup = BeautifulSoup(response.content, "html.parser")

        # Loop through each news short on the page and extract the title, content, and category
        for news_card in soup.find_all("div", itemtype="http://schema.org/NewsArticle"):
            title = news_card.find("span", itemprop="headline").text
            content = news_card.find("div", itemprop="articleBody").text
            category = cat.capitalize()

            # Create a dictionary containing the title, content, and category of the news short
            short = {"title": title, "content": content, "category": category}

            # Append the news short dictionary to the list of shorts
            shorts.append(short)

    # Create a pandas DataFrame from the list of news shorts and cache the data to a CSV file
    shorts_df = pd.DataFrame(shorts)
    shorts_df.to_csv("csv_files/" + filename, index=False)

    # Return the pandas DataFrame containing the news short titles, content, and categories
    return shorts_df
