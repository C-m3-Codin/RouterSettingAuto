# http://192.168.1.1/boaform/formDhcpServer
# 192.168.1.1/boaform/formDhcpServer


from bs4 import BeautifulSoup
import requests
session =requests.session()
url="http://192.168.1.1"
html_content = session.get(url).text
print(html_content[641:646])
verificationCo=html_content[641:646]
pyload_auth={'username':'admin','psd':'admin@123','verification_code':verificationCo}
s = session.post("http://192.168.1.1/boaform/admin/formLogin_en",data=pyload_auth)
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
s = session.post("http://192.168.1.1/boaform/formDhcpServer",data=payload_dns_block_cloudfare_google)
print(s.text)