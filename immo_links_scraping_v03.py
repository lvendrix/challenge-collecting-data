from typing import Text
import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import requests
from threading import Thread, RLock
import time
import random
from random import randint
import csv


#Threads to get all houses links and write it to a txt file:
class ImmoLinks(Thread):
    def __init__(self, link):
        Thread.__init__(self)
        self.link = link

    def run(self):
        driver.get(self.link)
        soup = BeautifulSoup(driver.page_source, features='lxml')
        for elem in soup.find_all('a', attrs={"class": "card__title-link"}):
            txt_list = open("./houses_links.txt", 'a')
            txt_list.write(elem.get("href"))
            txt_list.write("\n")


#Web scraping
driver = webdriver.Chrome(executable_path='C:\Program Files\Google\Chrome\Application\chromedriver.exe')

#Click the cookies button after open website:
driver.get('https://www.immoweb.be/en/search/house/for-sale?countries=BE&page=1&orderBy=relevance')
time.sleep(random.uniform(1.0, 4.0))
cookie_button = driver.find_element_by_xpath('/html/body/div[4]/div[4]/div[2]/div/div[2]/div[1]/button')
cookie_button.click()
time.sleep(random.uniform(1.0, 2.0))

#Get all houses links from immoweb "for-sale" page=1:
soup = BeautifulSoup(driver.page_source, features='lxml')
for elem in soup.find_all('a', attrs={"class": "card__title-link"}):
    txt_list = open("./houses_links.txt", 'a')
    txt_list.write(elem.get("href"))
    txt_list.write("\n")

index = 2
for item in range(331):
    immo_url = 'https://www.immoweb.be/en/search/house/for-sale?countries=BE&page=1&orderBy=relevance'
    next_url = immo_url.replace('page=1', f'page={index}')
    thread = ImmoLinks(next_url)
    thread.start()
    thread.join()
    index += 1

