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

def changePass(ssid,newPass):
    if(ssid=="kf"):
        # 
        indx="1"
        print("changed kfon password")
    elif(ssid=="kf2"):
        # 
        indx="1"
        print("changed kfon2 pass")
    elif(ssid=="kfbr"):
        # 
        indx="0"
        print("password of broad changed")
    load={
	"wlanDisabled": "OFF",
	"isNmode": "1",
	"wpaSSID": indx,
	"security_method": "6",
	"auth_type": "both",
	"wepEnabled": "ON",
	"length0": "1",
	"format0": "1",
	"key0": "*****",
	"wpaAuth": "psk",
	"dotIEEE80211W": "1",
	"sha256": "0",
	"ciphersuite_t": "1",
	"wpa2ciphersuite_a": "1",
	"gk_rekey": "86400",
	"pskFormat": "0",
	"pskValue": newPass,
	"wapiPskFormat": "0",
	"wapiPskValue": "",
	"wepKeyLen": "wep64",
	"radiusIP": "0.0.0.0",
	"radiusPort": "1812",
	"radiusPass": "",
	"wapiASIP": "0.0.0.0",
	"wlan_idx": "0",
	"submit-url": "/wlwpa_en.asp",
	"save": "Apply+Changes"
    }
    s = session.post("http://192.168.1.1/boaform/admin/formWlEncrypt",data=load)
    
    print(s.text)


pyload={'username':'admin','psd':'admin@123','verification_code':verificationCo}
s = session.post("http://192.168.1.1/boaform/admin/formLogin_en",data=pyload)

# list_clients()
# changeDns("noBlock")
# changeDns("block")
# changePass("kfbr","payforpasswordbroad2112")


