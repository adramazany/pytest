import requests
import os
from requests.auth import HTTPProxyAuth
from urllib3.exceptions import InsecureRequestWarning

proxy = 'http://ramezania:R%40mezani25@proxy-roding.ger.muehlbauer.de:8080'
# proxy = sys.argv[2]
os.environ['http_proxy'] = proxy
os.environ['HTTP_PROXY'] = proxy
os.environ['https_proxy'] = proxy
os.environ['HTTPS_PROXY'] = proxy
# r = requests.get("https://www.google.com/", verify=False, timeout=10)
r = requests.get("https://www.verbformen.de/?w=gehen", verify=False, timeout=10)

# proxies = {"http":"proxy-roding.ger.muehlbauer.de:8080"}
# auth = HTTPProxyAuth("ramezania", "R@mezani25")

# r = requests.get("http://www.google.com/", proxies=proxies, auth=auth)
# r = requests.get("https://www.google.com/", proxies=proxies, auth=auth, verify=False, timeout=10)
# r = requests.get("https://www.verbformen.de/?w=gehen", proxies=proxies, auth=auth,headers=headers, cookies=cookies)
# requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
# r = requests.get("https://www.verbformen.de", proxies=proxies, auth=auth, verify=False, timeout=5)
print(r.status_code)
print(r.content)