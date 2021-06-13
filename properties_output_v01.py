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
import pandas as pd


class PropertyLinks(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        #Logan's code here to extract house data:
        list_results = []
        with open("C:\\Users\\joser\\BeCode_Course\\03_Python\\Assignments\\collecting_data\\challenge-collecting-data\\houses_provinces\\houses_antwerp_test.txt", "r+", encoding="utf-8") as links:
            while links:
                url = links.readline()
                list_results.append(url_information(url))
                keys = list_results[0].keys()
                a_file = open("output.csv", "a", encoding="utf-8")
                dict_writer = csv.DictWriter(a_file, keys)
                dict_writer.writeheader()
                dict_writer.writerows(list_results)


def url_information(url):
    driver = webdriver.Chrome(executable_path='C:\Program Files\Google\Chrome\Application\chromedriver.exe')
    #Selenium + BeautifulSoup way
    driver.get(url)
    q = BeautifulSoup(driver.page_source, features='lxml')

    result = {}

    # Subtype of property
    for element in q("h1.classified__title"):
        # subtype = (element.text.strip().split(' ', 1)[0])
        subtype = (element.text.strip().split(' for')[0]).replace("\n ", "").strip()
        result.update({'Subtype of property': subtype})

    # print(result)
    # Price
    for element in q("p.classified__price span"):
        price = (element.text.strip().split(' ', 1))[0]
        # price_clean = ""
        # for char in price:
        #    if char.isdigit():
        #        price_clean.join

        # print(price)
        # result.append({"name": "Price", "value": price})

    # Location, # of frontages, Living area, Kitchen type, # of bedrooms, Furnished, Surface of the plot, State of the building, Garden

    for element in q("tr.classified-table__row"):
        th_element = element.find("th")
        td_element = element.find("td")

        name = None
        value = None

        if th_element is not None:
            name = th_element.text.strip()
        if td_element is not None:
            value = td_element.text.strip()

        result.update({name: value})

    # Formatting the data
    house_subtypes = [
        "House",
        "Bungalow",
        "Chalet",
        "Castle",
        "Farmhouse",
        "Country house",
        "Exceptional property",
        "Apartment block",
        "Mixed-use building",
        "Town-house",
        "Mansion",
        "Villa",
        "Other properties",
        "Manor house",
        "Pavilion"
    ]

    apartment_subtypes = [
        "Ground floor",
        "Duplex",
        "Triplex",
        "Studio",
        "Penthouse",
        "Loft",
        "Kot",
        "Service flat"
    ]

    if "Garden" in result or 'Garden surface' in result:
        result["Garden"] = 1
    else:
        result.update({"Garden": 0})
        result.update({"Garden surface": 0})

    if "Furnished" in result:
        if result["Furnished"] == 'Yes':
            result["Furnished"] = 1
        elif result["Furnished"] == 'No':
            result["Furnished"] = 0
    else:
        result.update({"Furnished": 0})

    if 'How many fireplaces?' in result:
        result.update({"Open fire": 1})
    else:
        result.update({"Open fire": 0})

    if "Swimming pool" in result:
        result["Swimming Pool"] = 1
    else:
        result.update({"Swimming Pool": 0})

    if 'Terrace surface' in result:
        result.update({"Terrace": 1})
    else:
        result.update({"Terrace": 0})
        result.update({"Terrace surface": None})

    if 'Surface of the plot' not in result:
        result.update({'Surface of the plot': None})

    if 'Kitchen type' in result:
        result.update({'Fully equipped kitchen' : 1})
    else:
        result.update({'Fully equipped kitchen' : 0})

    if 'Neighbourhood or locality' in result:
        result.update({'Locality': result['Neighbourhood or locality'].title()})
    else:
        result.update({'Locality': None})

    if 'Building condition' not in result:
        result.update({'Building condition': None})

    #if result['Subtype of property'] in house_subtypes:
    #    result.update({'Type of property': 'House'})
    #elif result['Subtype of property'] in apartment_subtypes:
    #    result.update({'Type of property': 'Apartment'})

    # Cleaning the data
    wishlist_keys = [
        'Type of property',
        'Subtype of property',
        'Building condition',
        'Locality',
        'Surface of the plot',
        'Living area',
        'Bedrooms',
        'Furnished',
        'Fully equipped kitchen',
        'Number of frontages',
        'Garden',
        'Garden surface',
        'Swimming Pool',
        'Open fire',
        'Terrace',
        'Terrace surface']

    result_clean = dict.fromkeys(wishlist_keys)
    for key, value in result.items():
        if key in wishlist_keys:
            result_clean[key] = value
        
    #print(result)
    print(result_clean)
    return result_clean

    """
    Some information is not always present for each property:
    - Garden: Y/N > CHECK First if present or not, if nothing: if Garden Area != None, then Garden == Y, else Garden == N
    - Garden Area > if not mentioned, we assume there is NO Garden Area
    - Swimming Pool: Y/N > if not mentioned (None), we assume there is NO swimming pool
    - Terrace: Y/N > CHECK First if present or not, if nothing: if Terrace Area != None, then Terrace == Y, else Terrace == N
    - Terrace Area > if not mentioned, we assume there is No Terrace Area
    - Open fire: Y/N > if not mentioned (None), we assume there is NO open fire
 
    """

thread = PropertyLinks()
thread.start()
thread.join()