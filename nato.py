import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import time
from PIL import Image
from io import BytesIO
import os
import random
import pandas as pd

home_url = "https://manganato.com/"
image_site = "https://chapmanganato.com/"

respense = requests.get(home_url)

xml = respense.text
soup = BeautifulSoup(xml,"html")

manga_list = soup.find_all("div", class_="content-homepage-item")

dict = {}
for manga in manga_list:
    name = manga.find("a")["title"]
    url = (manga.find("a")["href"])
    dict[name] = url

# create a pandas dataframe with colmns: name, cahpter, views, date.
chapterData = pd.DataFrame(columns=["name","chapter","views","date"])
# create a pandas dataframe for the manga: name, genre, author, status.
mangaData = pd.DataFrame(columns=["name","genre","author","status"]) 

for name, url in dict.items():
    
    # get the manga page
    manga_page = requests.get(url)
    manga_soup = BeautifulSoup(manga_page.text,"html")
    list = manga_soup.find_all("li", class_="a-h") 
    # get the manga info
    for item in list:
        if item.find("span").text == "Genre":
            genre = item.find("a").text
        elif item.find("span").text == "Author(s)":
            author = item.find("a").text
        elif item.find("span").text == "Status":
            status = item.find("a").text
    # get the manga chapters
    chapter_list = manga_soup.find_all("li", class_="a-h")
    for chapter in chapter_list:
        if chapter.find("a") != None:
            chapter_name = chapter.find("a")["title"]
            chapter_url = chapter.find("a")["href"]
            chapter_views = chapter.find("span").text
            chapter_date = chapter.find("i").text
            chapterData = chapterData.append({"name":name,"chapter":chapter_name,"views":chapter_views,"date":chapter_date},ignore_index=True)
    mangaData = mangaData.append({"name":name,"genre":genre,"author":author,"status":status},ignore_index=True) 
    # get the manga cover
    cover = manga_soup.find("div", class_="manga-info-pic")
    cover_url = cover.find("img")["src"]
    cover_name = name + ".jpg"

    # 





    break