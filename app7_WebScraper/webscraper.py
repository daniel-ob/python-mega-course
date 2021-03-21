import re

import requests
from bs4 import BeautifulSoup

# Using cached version of www.century21.com, search "Rock Springs, WY"
# Header allows to impersonate a web browser
r = requests.get("http://www.pyclass.com/real-estate/rock-springs-wy/LCWYROCKSPRINGS/",
                 headers={'User-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0'})
c = r.content
soup = BeautifulSoup(c, "html.parser")

# find all property rows on first results page
rows = soup.find_all("div", {"class": "propertyRow"})
# print(len(rows))

# parse property fields
for row in rows:
    address = row.find_all("span", {"class": "propAddressCollapse"})[0].text

    area = row.find("span", {"class": "infoSqFt"})
    area = area.find("b").text if area else None

    beds = row.find("span", {"class": "infoBed"})
    beds = beds.find("b").text if beds else None

    full_baths = row.find("span", {"class": "infoValueFullBath"})
    full_baths = full_baths.find("b").text if full_baths else None

    half_baths = row.find("span", {"class": "infoValueHalfBath"})
    half_baths = half_baths.find("b").text if half_baths else None

    locality = row.find_all("span", {"class": "propAddressCollapse"})[1].text

    lot_size = None
    for column_group in row.find_all("div", {"class": "columnGroup"}):
        for feature_group in column_group.find_all("span", {"class": "featureGroup"}):
            if "Lot Size" in feature_group.text:
                lot_sizes = column_group.find_all("span", {"class": "featureName"})
                lot_size = lot_sizes[0].text + lot_sizes[1].text if len(lot_sizes) == 2 else lot_sizes[0].text
                continue

    mls = row.find("div", {"class": "propertyMLS"}).text
    mls = re.sub(r'[\n ]', '', mls)
    mls = re.sub('MLS#', '', mls)

    price = row.find("h4", {"class": "propPrice"}).text
    price = re.sub(r'[\n ]', '', price)

    print(address, area, beds, full_baths, half_baths, locality, lot_size, mls, price)
