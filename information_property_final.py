import requests
from pyquery import PyQuery

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
        result.update({'Fully equipped kitchen' : 0})

    # Locality
    if 'Neighbourhood or locality' in result:
        result.update({'Locality': result['Neighbourhood or locality'].title()})
    else:
        result.update({'Locality': None})

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

    # Calculating the land area (= Surface of the plot - surface garden - surface terrace)
    if result['Surface of the plot'] != None and result['Terrace surface'] != None and result['Garden surface'] != None:
        result.update({'Surface of the land': int(result['Surface of the plot']) - int(result['Terrace surface']) - int(result['Garden surface'])})
    elif result['Surface of the plot'] != None and result['Terrace surface'] != None and result['Garden surface'] == None:
        result.update({'Surface of the land': int(result['Surface of the plot']) - int(result['Terrace surface'])})
    else:
        result.update({'Surface of the land': None})

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

    if result['Subtype of property'] in house_subtypes:
        result.update({'Type of property': 'House'})
    elif result['Subtype of property'] in apartment_subtypes:
        result.update({'Type of property': 'Apartment'})
    elif result['Subtype of property'] in office_subtypes:
        result.update({'Type of property': 'Office'})
    elif result['Subtype of property'] in business_subtypes:
        result.update({'Type of property': 'Business'})
    elif result['Subtype of property'] in industry_subtypes:
        result.update({'Type of property': 'Industry'})
    else:
        result.update({'Type of property': None})

    # Type of sales (Investment property or not)
    if result['Investment property'] == 'Yes':
        result['Investment property'] = 1
    elif result['Investment property'] == 'No':
        result['Investment property'] = 0

    # Cleaning the data to only keep the desired features
    wishlist_keys = [
        'Type of property',
        'Subtype of property',
        'Price',
        'State of the building',
        'Locality',
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
            
    print(result_clean)
    return result_clean

""" HERE YOU HAVE TO PUT THE LINKS"""

list_results = []
links = ["https://www.immoweb.be/en/classified/bungalow/for-sale/huy/4500/9373744?searchId=60c225a3df9c5",
         "https://www.immoweb.be/en/classified/villa/for-sale/wavre/1300/9372293?searchId=60c35f939b343",
         "https://www.immoweb.be/en/classified/house/for-sale/leuven/3000/9375243?searchId=60c35e6953213",
         "https://www.immoweb.be/en/classified/villa/for-sale/rhode-st-genese/1640/9379683?searchId=60c72e3c449a1",
         "https://www.immoweb.be/en/classified/villa/for-sale/brecht/2960/9380210?searchId=60c73b94329b1",
         "https://www.immoweb.be/en/classified/apartment-block/for-sale/etterbeek/1040/9381221?searchId=60c74b4885721"
]

for url in links:
    list_results.append(url_information(url))
