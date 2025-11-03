import requests
from requests.auth import HTTPProxyAuth
from bs4 import BeautifulSoup

url = 'https://www.verbformen.de/?w=gehen'
proxies = {"http":"proxy-roding.ger.muehlbauer.de:8080"}
auth = HTTPProxyAuth("ramezania", "R@mezani25")

r = requests.get(url, proxies=proxies, auth=auth)
print(r.content)


soup = BeautifulSoup(r.content)
print(soup.prettify())

# #x3c2d7
