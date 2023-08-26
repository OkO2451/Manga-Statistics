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
latest_url =  "https://manganato.com/genre-all/"


dict = {}
# gathering manga list from top 50 pages
for i in range(1,51):
    # slow down the request
    time.sleep(random.randint(1,3) + random.randint(1,9)*0.1)
    # allow redirect
    respense = requests.get(latest_url+str(i), allow_redirects=True)
    # get the html
    html = respense.text
    # parse the html
    soup = BeautifulSoup(html,"html")
    # get the list of manga
    manga_list = soup.find_all("div", class_="content-homepage-item")
    # the dictionary is already created 
    # TODO: make the dictionary a class
    for manga in manga_list:
        name = manga.find("a")["title"]
        url = (manga.find("a")["href"])
        dict[name] = url




# create a pandas dataframe with colmns: name, cahpter, views, date.
chapterData = pd.DataFrame(columns=["name","chapter","views","date"])
# create a pandas dataframe for the manga: name, genre, author, status.
mangaData = pd.DataFrame(columns=["name","genre","author","status","alt_title","views","score",'nb_votes']) 

dictManga = {"name":"",
             "genre":"",
             "author":"",
             "status":"",
             "alt_title":"",
             "views":"",
             "score":"",
             "nb_votes":""
             }
dictChapter = {"name":"",
                "chapter":"",
                "views":"",
                "date":""
                }
for name, url in dict.items():
    
    
    # get the manga page
    manga_page = requests.get(url)
    manga_soup = BeautifulSoup(manga_page.text,"html")
    manga_info = manga_soup.find("table", class_="variations-tableInfo")
    for name, url in dict.items():
        # based on aug 26th 2023 
        # get the manga page
        manga_page = requests.get(url)
        manga_soup = BeautifulSoup(manga_page.text,"html")
        manga_info = manga_soup.find("table", class_="variations-tableInfo")
        dictManga["name"] = name
        dictManga["genre"] = manga_info.find_all("tr")[3].find("td", class_="table-value").text.strip().replace(" ","")
        dictManga["author"] = manga_info.find_all("tr")[1].find("td", class_="table-value").text 
        dictManga["status"] = manga_info.find_all("tr")[2].find("td", class_="table-value").text
        dictManga["alt_title"] = manga_info.find_all("tr")[0].find("td", class_="table-value").text
        dictManga["views"] = manga_soup.find_all("span",class_="stre-value")[1].text
        dictManga["score"] = manga_soup.find_all("em")[7].text.strip()
        dictManga["nb_votes"] = manga_soup.find_all("em")[9].text
        mangaData = pd.concat([mangaData, pd.DataFrame([dictManga])], ignore_index=True)
    # get the manga chapters

    list = manga_soup.find_all("li", class_="a-h") 
    # get the manga info
    for a in list:
        # add to the dict
        dictChapter["name"] = name
        dictChapter["chapter"] = a.find('a', {'class': 'chapter-name'}).text
        dictChapter["views"] = a.find('span', {'class': 'chapter-view'}).text
        dictChapter["date"] = a.find('span', {'class': 'chapter-time'})["title"]
        # add to the dataframe
        chapterData = chapterData.append(dictChapter,ignore_index=True)





    break