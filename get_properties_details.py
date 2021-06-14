import csv
import pandas as pd
from pyquery import PyQuery
from selenium import webdriver
from threading import Thread, RLock

lock = RLock()

class PropertyThread(Thread):
    '''This class will be used to do threading for every single
       property link. As grabbing all details for property will
       take some time, so threading will increase data collection speed
    '''
    def __init__(self, url):
        Thread.__init__(self)
        self.url = url
    
    def run(self):
        with lock:
            print("Proccessing url: ", self.url)
            property_info = get_property_details(self.url)

            if property_info:
                all_properties_details.append(property_info)
                print("Done")
            else:
                print("Skipped")
                
                
def get_property_details(url):
    
    driver = webdriver.Chrome()
    driver.get(url)
    if driver.get_log('browser'):
        #url not correct
        driver.close()
    else:
        # let's grap the html for the correct url
        html = PyQuery(driver.page_source)

        result = {}
        property_details = {}
        
        # grab the locality
        locality = list(html.items('span.classified__information--address-row'))[1].text()
        result['Locality'] = locality
        
        # the type of property is House by default
        result['Type_of_property'] = 'House'
        
        # grab the subtype
        subtitle = list(html('h1.classified__title'))[0].text.strip().split('for')[0].strip()
        
        # check if it's an apartment subtype
        if subtitle in Subtype_of_Apartments:
            result['Type_of_property'] = 'Apartment'
        result['Subtype_of_property'] = subtitle
        
        # let's focus only on House and Apartment 
        if (subtitle in Subtype_of_house) or (subtitle in Subtype_of_Apartments):
            # Standart or default type of sale is None (nothing)
            type_of_sale = None
            # check for type of sale
            for item in html('div.flag-list__item--secondary span'):
                if item.text:
                    type_of_sale = item.text
            result['Type_of_sale'] = type_of_sale
            
            # grab the price
            for item in html('p.classified__price span'):
                price = None
                if item.text and item.text[-1] == '€':
                    price = item.text[:-1]
                result['Price'] = price
            
            # grab the rest of information
            for item in html.items('tr.classified-table__row'):
                item_list = item.text().split('\n')
                name = None
                value = None
                if item_list[0]:
                    name = item_list[0]
                    value = item_list[1]
                    result[name] = value

            driver.close()

            if 'Living area' in result:
                result['Area'] = result.pop('Living area')
                result['Area'] = result['Area'].split()[0]
            else:
                result['Area'] = None
            if 'Building condition' in result:
                result['Building_condition'] = result.pop('Building condition')
            else:
                result['Building_condition'] = None
            if 'Number of frontages' in result:
                result['Number_of_facades'] = result.pop('Number of frontages')
            else:
                result['Number_of_facades'] = None
            if 'Kitchen type' in result:
                result['Kitchen_type'] = result.pop('Kitchen type')
            else:
                result['Kitchen_type'] = None

            if 'How many fireplaces?' in result:
                result['Open_fire'] = result.pop('How many fireplaces?')
            else:
                result['Open_fire'] = '0'
            if 'Terasse surface' in result:
                result['Terasse'] = result.pop('Terasse surface')
                result['Terasse'] = result['Terasse'].split()[0]
            else:
                result['Terasse'] = '0'
            if 'Garden surface' in result:
                result['Garden'] = result.pop('Garden surface')
                result['Garden'] = result['Garden'].split()[0]
            else:
                result['Garden'] = '0'
            if 'Swimming pool' in result:
                result['Swimming_pool'] = result.pop('Swimming pool')
                result['Swimming_pool'] = '1'
            else:
                result['Swimming_pool'] = '0'
            if 'Surface of the plot' in result:
                result['Surface_of_land'] = result.pop('Surface of the plot')
                result['Surface_of_land'] = result['Surface_of_land'].split()[0]
            else:
                result['Surface_of_land'] = None
            if 'Total ground floor buildable' in result:
                result['Surface_plot_land'] = result.pop('Total ground floor buildable')
                result['Surface_plot_land'] = result['Surface_plot_land'].split()[0]
            else:
                result['Surface_plot_land'] = None
            if 'Furnished' not in result:
                result['Furnished'] = 'No'
            if 'Bedrooms' in result:
                result['Number_of_rooms'] = result.pop('Bedrooms')
            else:
                result['Number_of_rooms'] = '0'
            for key in columns:
                property_details[key] = result[key]

            return property_details
        else:
            driver.close()

Type_of_property_not_checked = ["Garage", "Office", "Business", "Industry", "land", "Tenement", "Other",
                   "New real estate project - Houses", "New real estate project - Apartments"]
Building_condition_lst = ["Good", "To restore", "To be done up", "As new", "Just renovated", "To renovate"]
Type_of_sale_lst = ["Include new build", "Include public sales", "Include life annuity sales", "Investment property"]
Subtype_of_house = ["House", "Apartment block", "Bungalow", "Chalet", "Castle", "Farmhouse", "Country house", "Exceptional property", "Mixed-use building", 
           "Town-house", "Mansion","Villa", "Other properties", "Manor house", "Pavilion"]
Subtype_of_Apartments = ["Ground floor", "Triplex", "Penthouse", "Kot", "Duplex", "Studio", "Loft", "Service flat"]
columns = ["Type_of_property", "Subtype_of_property", "Locality", "Price", "Type_of_sale", "Number_of_rooms", "Area", "Kitchen_type",
          "Furnished", "Open_fire", "Terasse", "Garden", "Surface_of_land", "Surface_plot_land", "Number_of_facades", "Swimming_pool",
          "Building_condition"]
all_properties_details = []