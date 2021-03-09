
from bs4 import BeautifulSoup
import requests
session =requests.session()
url="http://192.168.1.1"
html_content = session.get(url).text
print(html_content[641:646])
verificationCo=html_content[641:646]

def list_clients():
    clients=session.get('http://192.168.1.1/wlstatbl_en.asp')
    # print(clients.text)
    soup = BeautifulSoup(clients.text, 'html.parser')
    # print(soup)
    tables = soup.findChildren('table')
    # print(tables[1])
    my_table = tables[1]
    rows = my_table.findChildren(['th', 'tr'])
    for row in rows:
        cells = row.findChildren('td')
        print(cells[0].string)
        # for cell in cells:
        #     value = cell.string
        #     print("value + "+ value + "\nvalue ended")
        # print(row)
        print("\n")
# print(soup)

pyload={'username':'admin','psd':'admin@123','verification_code':verificationCo}
s = session.post("http://192.168.1.1/boaform/admin/formLogin_en",data=pyload)
# print(s.text)
# s = session.get('http://192.168.1.1')
# soup = BeautifulSoup(s.text, 'html.parser')
# print(s.text)
list_clients()


