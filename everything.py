import requests
import datetime
import json
from dateutil import parser
from bs4 import BeautifulSoup
import openai
openai.api_key = "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"

# getURL scrapes a website for the URLs to all the News Articles from today
def getURL():
    #make this a user input so the URL can be from any wesbite?
    url = "https://thehackernews.com/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    # Get today's date
    today = datetime.datetime.now().date()

    # Find all articles with class "story-link"
    URLs = []
    articles = soup.find_all("a", class_="story-link")
    for article in articles:
        link = article.get("href")
        try:
            date_string = article.find("span", class_="h-datetime").text.strip()[1:]
            date = parser.parse(date_string).date()
        except:
            continue
        if date == today:
            URLs.append(link) 
    return URLs


# Gets the article title and text from the url
def get_article_title(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    article_title = soup.find('h1').get_text()
    return article_title

def get_article_text(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    all_paragraphs = soup.find_all('p')
    article_text = ""
    for p in all_paragraphs:
        article_text += p.get_text()
    return article_text

# Create an empty list to store the article summaries
def createSummaries():
    articlesAndText = []
    for article in getURL():
        article_title = get_article_title(article)
        article_text = get_article_text(article)
        articlesAndText.append({'article': article_title, 'summary': article_text})
    return articlesAndText
    
# Create the Podcast Script
def podcastScript():
    prompt = createSummaries()
    
    response2 = openai.Completion.create(
        model="text-davinci-003", 
        prompt=f"The following is a dictionary with multiple keys and two arguments. Build me a podcast script using this dictionary for the main content and make sure every key is used in its own section of the podcast.  Each section should be 4-5 sentences long.Iinclude an introduction and conclusion for the podcast: {prompt}",
        temperature=0,
        max_tokens=1000,
        top_p=1,
        frequency_penalty=.25,
        presence_penalty=0)
    podcast = response2["choices"][0]["text"]
    print(podcast)

if __name__ == '__main__':
    podcastScript()


dan