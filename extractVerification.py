from bs4 import BeautifulSoup
import requests
url="http://192.168.1.1"
html_content = requests.get(url).text
print(html_content[641:646])