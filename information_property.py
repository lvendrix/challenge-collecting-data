import requests
from pyquery import PyQuery
import csv

url ='https://www.immoweb.be/en/classified/bungalow/for-sale/huy/4500/9373744?searchId=60c277c849adwja'
response = requests.get(url)
# Checks if proper url
response.raise_for_status()

q = PyQuery(response.text)

result = []

for element in q("tr.classified-table__row"):
    th_element = element.find("th")
    td_element = element.find("td")

    name = None
    value = None

    if th_element is not None:
        name = th_element.text.strip()
    if td_element is not None:
        value = td_element.text.strip()

    result.append({"name": name, "value": value})

print(result)

"""
for elem in result:
    if elem['name'] == 'Address':
        print(elem['value'])

with open("results.csv",'w', newline ='') as file:
    wr = csv.writer(file, quoting = csv.QUOTE_ALL)
    wr.writerow(result)
"""