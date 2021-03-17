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
print(len(rows))
