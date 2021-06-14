import requests
from pyquery import PyQuery
import csv
from selenium import webdriver

def url_information(url):
    response = requests.get(url)
    q = PyQuery(response.text)
    result = {}

    # Getting most of the desired features located in tables on the page
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

    # Subtype of property (not in a table)
    for element in q("h1.classified__title"):
        subtype = (element.text.strip().split(' for')[0]).replace("\n ", "").strip()
        result.update({'Subtype of property': subtype})

    # Price (not in a table)
    for element in q("p.classified__price span.sr-only"):
        price = (element.text[:-1])
        price_clean_list = []
        for char in price:
            if char.isdigit():
                price_clean_list.append(char)
        price_clean = ''.join(price_clean_list)
        result.update({'Price': price_clean})

    # Formatting the data
    # Garden
    if "Garden" in result or 'Garden surface' in result:
        result["Garden"] = 1
    else:
        result.update({"Garden": 0})
        result.update({"Garden surface": None})

    # Furnished
    if "Furnished" in result:
        if result["Furnished"] == 'Yes':
            result["Furnished"] = 1
        elif result["Furnished"] == 'No':
            result["Furnished"] = 0
    else:
        result.update({"Furnished": 0})
    # Fireplace

    if 'How many fireplaces?' in result:
        result.update({"Open fire": 1})
    else:
        result.update({"Open fire": 0})

    # Terrace. If exists, its area. Otherwise, None.
    if 'Terrace surface' in result:
        result.update({"Terrace": 1})
    else:
        result.update({"Terrace": 0})
        result.update({"Terrace surface": None})

    if 'Surface of the plot' not in result:
        result.update({'Surface of the plot': None})

    # Kitchen
    if 'Kitchen type' in result:
        if result['Kitchen type'] in ['Not installed', 'Semi equipped', 'Installed']:
            result.update({'Fully equipped kitchen': 0})
        else:
            result.update({'Fully equipped kitchen': 1})
    else:
        result.update({'Fully equipped kitchen': 0})

    # Building condition
    if 'Building condition' not in result:
        result.update({'Building condition': None})

    # Changing the name of 'Bedrooms' to 'Number of rooms'
    if 'Bedrooms' in result:
        result.update({'Number of rooms': result['Bedrooms']})

    # Changing the name of 'Number of frontages' to 'Number of facades'
    if 'Number of frontages' in result:
        result.update({'Number of facades': result['Number of frontages']})

    # Changing the name of 'Living area' to 'Area'
    if 'Living area' in result:
        result.update({'Area': result['Living area']})

    # Changing the name of 'Building condition' to 'State of the building'
    if 'Building condition' in result:
        result.update({'State of the building': result['Building condition']})



    # Subtype to Type. The actual type of the real estate is not mentionned. So we create a list for each type of properties.
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
        "Pavilion",
        "New real estate project - Houses"
    ]

    apartment_subtypes = [
        "Ground floor",
        "Duplex",
        "Triplex",
        "Studio",
        "Penthouse",
        "Loft",
        "Kot",
        "Service flat",
        "New real estate project - Apartments"
    ]

    office_subtypes = [
        "Offices",
        "Building",
        "Office block",
        "Mixed - use building offices",
        "Large town house",
        "Commercial villa",
    ]

    business_subtypes = [
        "Commercial premises",
        "Mixed use building commercial",
        "Catering industry"
    ]

    industry_subtypes = [
        "Industrial premises",
        "Mixed - use building",
        "Warehouse"
    ]

    # Cleaning the data to only keep the desired features
    wishlist_keys = [
        'Type of property',
        'Subtype of property',
        'Price',
        'State of the building',
        'Surface of the plot',
        'Surface of the land',
        'Area',
        'Number of rooms',
        'Furnished',
        'Fully equipped kitchen',
        'Number of facades',
        'Garden',
        'Garden surface',
        'Open fire',
        'Terrace',
        'Terrace surface',
        'Investment property'
    ]

    result_clean = dict.fromkeys(wishlist_keys)
    for key, value in result.items():
        if key in wishlist_keys:
            result_clean[key] = value

    # Type of sales (Investment property or not)
    if result_clean['Investment property'] == 'Yes':
        result_clean['Investment property'] = 1
    elif result_clean['Investment property'] == 'No':
        result_clean['Investment property'] = 0

    if result_clean['Subtype of property'] in house_subtypes:
        result_clean.update({'Type of property': 'House'})
    elif result_clean['Subtype of property'] in apartment_subtypes:
        result_clean.update({'Type of property': 'Apartment'})
    elif result_clean['Subtype of property'] in office_subtypes:
        result_clean.update({'Type of property': 'Office'})
    elif result_clean['Subtype of property'] in business_subtypes:
        result_clean.update({'Type of property': 'Business'})
    elif result_clean['Subtype of property'] in industry_subtypes:
        result_clean.update({'Type of property': 'Industry'})
    else:
        result_clean.update({'Type of property': None})

    if result_clean['Surface of the plot'] != None and result_clean['Terrace surface'] != None and result_clean['Garden surface'] != None:
        result_clean.update({'Surface of the land': int(result_clean['Surface of the plot']) - int(result_clean['Terrace surface']) - int(result_clean['Garden surface'])})
    elif result_clean['Surface of the plot'] != None and result_clean['Terrace surface'] != None and result_clean['Garden surface'] == None:
        result_clean.update({'Surface of the land': int(result_clean['Surface of the plot']) - int(result_clean['Terrace surface'])})
    elif result_clean['Surface of the plot'] != None and result_clean['Terrace surface'] == None and result_clean['Garden surface'] != None:
        result_clean.update({'Surface of the land': int(result_clean['Surface of the plot']) - int(result_clean['Garden surface'])})
    elif result_clean['Surface of the plot'] != None and result_clean['Terrace surface'] == None and result_clean['Garden surface'] == None:
        result_clean.update({'Surface of the land': result_clean['Surface of the plot']})
    else:
        result_clean.update({'Surface of the land': None})

    print(result_clean)
    return result_clean

""" HERE YOU HAVE TO PUT THE LINKS"""

list_results = []
with open("./belgium_properties.txt", "r", encoding="utf-8") as links:
    for line in range(5001):
        url = links.readline()
        url = url.strip('\n')
        list_results.append(url_information(url))
        keys = list_results[0].keys()
        a_file = open("output_5000.csv", "w", encoding="utf-8")
        dict_writer = csv.DictWriter(a_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(list_results)
        a_file.close()






