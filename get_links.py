import os
from pyquery import PyQuery
from selenium import webdriver 
from threading import Thread, RLock

lock = RLock()
links_path = os.path.abspath('./')
new_file_path = os.path.join(links_path, 'all_properties_links.txt')

class LinksThread(Thread):
    def __init__(self, link):
        Thread.__init__(self)
        self.link = link
    
    def run(self):
        with lock:
            with open(new_file_path, 'a', encoding='utf-8') as new_file:
                new_file.write(self.link + '\n')
                

def get_house_links(page_number):
    '''This function iterates immoweb pages for houses to buy from page 1 to page_number < 333.
       Then its collecte all houses links for every single page and save them in a .txt file
       through LinksThreading.
    '''
    for n in range(1,page_number):
        url = f"https://www.immoweb.be/en/search/house/for-sale?countries=BE&page={n}&orderBy=relevance"
        driver = webdriver.Chrome()
        driver.get(url)
        html = PyQuery(driver.page_source)

        for item in html('a.card__title-link'):
            link = item.get('href')
            thread = LinksThread(link)
            thread.start()
            thread.join()
        driver.close()

def get_apartment_links(page_number):
    '''This function iterates immoweb pages for apartments to buy from page 1 to page_number < 333.
       Then its collecte all apartments links for every single page and save them in a .txt file
       through LinksThreading.
    '''
    for n in range(1,page_number):
        url = f"https://www.immoweb.be/en/search/apartment/for-sale?countries=BE&page={n}&orderBy=relevance"
        driver = webdriver.Chrome()
        driver.get(url)
        html = PyQuery(driver.page_source)

        for item in html('a.card__title-link'):
            link = item.get('href')
            thread = LinksThread(link)
            thread.start()
            thread.join()
        driver.close()