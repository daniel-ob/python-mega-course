import re

import requests
from bs4 import BeautifulSoup
import pandas


def get_soup(url):
    # Request header allows to impersonate a web browser
    user_agent = "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0"
    r = requests.get(url, headers={"User-agent": user_agent})
    c = r.content
    return BeautifulSoup(c, "html.parser")


# Using cached version of www.century21.com, search "Rock Springs, WY"
soup = get_soup("http://www.pyclass.com/real-estate/rock-springs-wy/LCWYROCKSPRINGS/")
nb_pages = len(soup.find("span", {"class": "PageNumbers"}).find_all("a", {"class": "Page"}))

# Store properties data in a list of dictionaries
props = []
url_base = "http://pyclass.com/real-estate/rock-springs-wy/LCWYROCKSPRINGS/t=0&s="
# 1st page "t=0&s=0.html", 2nd "t=0&s=10.html, 3rd "t=0&s=20.html ..."
for index in range(0, nb_pages * 10, 10):
    cur_url = url_base + str(index) + ".html"
    # print(cur_url)
    soup = get_soup(cur_url)

    # find all property rows on results page
    rows = soup.find_all("div", {"class": "propertyRow"})

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

    # print(len(props))

# Save data in a CSV file using a pandas DataFrame
df = pandas.DataFrame(props)
df.to_csv("output.csv")
