import re

import requests
from bs4 import BeautifulSoup
import pandas

# Using cached version of www.century21.com, search "Rock Springs, WY"
# Header allows to impersonate a web browser
r = requests.get("http://www.pyclass.com/real-estate/rock-springs-wy/LCWYROCKSPRINGS/",
                 headers={'User-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0'})
c = r.content
soup = BeautifulSoup(c, "html.parser")

# find all property rows on first results page
rows = soup.find_all("div", {"class": "propertyRow"})
# print(len(rows))

# Parse properties data, store it in a list of dictionaries
props = []
for row in rows:
    prop = {}

    address = row.find_all("span", {"class": "propAddressCollapse"})[0].text
    prop["Address"] = address

    area = row.find("span", {"class": "infoSqFt"})
    area = area.find("b").text if area else None
    prop["Area"] = area

    beds = row.find("span", {"class": "infoBed"})
    beds = beds.find("b").text if beds else None
    prop["Beds"] = beds

    full_baths = row.find("span", {"class": "infoValueFullBath"})
    full_baths = full_baths.find("b").text if full_baths else None
    prop["Full Baths"] = full_baths

    half_baths = row.find("span", {"class": "infoValueHalfBath"})
    half_baths = half_baths.find("b").text if half_baths else None
    prop["Half Baths"] = half_baths

    locality = row.find_all("span", {"class": "propAddressCollapse"})[1].text
    prop["Locality"] = locality

    lot_size = None
    for column_group in row.find_all("div", {"class": "columnGroup"}):
        for feature_group in column_group.find_all("span", {"class": "featureGroup"}):
            if "Lot Size" in feature_group.text:
                lot_sizes = column_group.find_all("span", {"class": "featureName"})
                lot_size = lot_sizes[0].text + lot_sizes[1].text if len(lot_sizes) == 2 else lot_sizes[0].text
                continue
    prop["Lot Size"] = lot_size

    mls = row.find("div", {"class": "propertyMLS"}).text
    mls = re.sub(r'[\n ]', '', mls)
    mls = re.sub('MLS#', '', mls)
    prop["MLS#"] = mls

    price = row.find("h4", {"class": "propPrice"}).text
    price = re.sub(r'[\n ]', '', price)
    prop["Price"] = price

    props.append(prop)

# Save data in a CSV file using a pandas DataFrame
df = pandas.DataFrame(props)
df.to_csv("output.csv")
