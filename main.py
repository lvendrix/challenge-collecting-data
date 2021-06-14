import os, csv
import pandas as pd
from pyquery import PyQuery
from selenium import webdriver 
from threading import Thread, RLock
from get_links import LinksThread, get_house_links, get_apartment_links
from get_properties_details import PropertyThread, get_property_details
from get_links import *
from get_properties_details import *


# try 10 pages
get_house_links(10)
# try 10 pages
get_apartment_links(10)

# let's grab all links from all_properties_links.txt file
# and store them in a list
urls = []

with open("./all_properties_links.txt") as links_file:
    links_list = links_file.readlines()
    for link in links_list:
        urls.append(link.strip('\n'))

# let's grab all properties information for every link
all_properties_details = []

for url in urls:
    thread = PropertyThread(url)
    thread.start()
    thread.join()

# now let's save all properties info in a csv file
with open('./all_properties_info.csv', 'w', encoding='UTF8', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=columns)
    writer.writeheader()
    writer.writerows(all_properties_details)