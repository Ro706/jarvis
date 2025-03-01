import requests
import pyttsx3
# import json
import datetime
import dotenv # Import dotenv module
import os
dotenv.load_dotenv()
engine = pyttsx3.init()
engine.setProperty('voice', engine.getProperty('voices')[0].id)
def speak(text):
    engine.say(text)
    engine.runAndWait()
class news:
    def __init__(self):
        self.url = f"https://newsapi.org/v2/top-headlines?country=us&category=business&apiKey={os.getenv('NEWS_API')}"
    def news(self):
        news=requests.get(self.url).json()
        article=news["articles"]
        news_article=[]
        for arti in article:
            news_article.append(arti["title"])
        print("Date : ",datetime.datetime.now().strftime("%d-%m-%Y"))
        print("News Report : ")
        for i in range(len(news_article)-13):
            a=i+1,news_article[i]
            print (i+1,news_article[i])
            speak(news_article[i])
            
def news_report():
    obj = news()
    obj.news()
    
if __name__ == "__main__":
    news_report()
