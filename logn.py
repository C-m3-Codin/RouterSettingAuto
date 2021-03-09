
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
        print("\n")
# print(soup)

def changeDns(dnsChoice):
    payload_dns_block_cloudfare_google={
	"uIp": "192.168.1.1",
	"uMask": "255.255.255.0",
	"uDhcpType": "1",
	"dhcpRangeStart": "192.168.1.2",
	"dhcpRangeEnd": "192.168.1.254",
	"ulTime": "86400",
	"ipv4landnsmode": "1",
	"Ipv4Dns1": "1.1.1.1",
	"Ipv4Dns2": "8.8.8.8",
	"submit-url": "http://192.168.1.1/net_dhcpd_en.asp"
    }
    payload_dns_block={
        "uIp": "192.168.1.1",
        "uMask": "255.255.255.0",
        "uDhcpType": "1",
        "dhcpRangeStart": "192.168.1.2",
        "dhcpRangeEnd": "192.168.1.254",
        "ulTime": "86400",
        "ipv4landnsmode": "1",
        "Ipv4Dns1": "192.168.1.14",
        "Ipv4Dns2": "198.168.1.14",
        "submit-url": "http://192.168.1.1/net_dhcpd_en.asp"
    }
    if(dnsChoice=="block"):
        dat=payload_dns_block
    elif (dnsChoice=="noBlock"):
        dat=payload_dns_block_cloudfare_google
    s = session.post("http://192.168.1.1/boaform/formDhcpServer",data=dat)
    print(s.text)

pyload={'username':'admin','psd':'admin@123','verification_code':verificationCo}
s = session.post("http://192.168.1.1/boaform/admin/formLogin_en",data=pyload)
# print(s.text)
# s = session.get('http://192.168.1.1')
# soup = BeautifulSoup(s.text, 'html.parser')
# print(s.text)
list_clients()


