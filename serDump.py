import flask
from flask import request as rq
print("bam")
from bs4 import BeautifulSoup
import requests
session =requests.session()
url="http://192.168.1.1"
html_content = session.get(url).text
print(html_content[641:646])
verificationCo=html_content[641:646]
pyload={'username':'admin','psd':'admin@123','verification_code':verificationCo}
s = session.post("http://192.168.1.1/boaform/admin/formLogin_en",data=pyload)
# list_clients()

# func to list clients
def list_clients():
    clients=session.get('http://192.168.1.1/wlstatbl_en.asp')
    # print(clients.text)
    soup = BeautifulSoup(clients.text, 'html.parser')
    # print(soup)
    tables = soup.findChildren('table')
    # print(tables[1])
    a=""
    my_table = tables[1]
    rows = my_table.findChildren(['th', 'tr'])
    for row in rows:
        cells = row.findChildren('td')
        print(cells[0].string)
        if(cells[0].string=="Mac Address"):
            continue
        else:
            a=a+"<h3>"+cells[0].string+" <button type=\"button\">block</button> <h3>"
        print("\n")
    return a
# print(soup)

# function to change password
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

# function to change dns
def changeDnsFunc(dnsChoice):
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

def switchToEnable():
    enableLoad={
	"macFilterEnble": "on",
	"action": "sw",
	"bcdata": "le",
	"submit-url": "http://192.168.1.1/secu_macfilter_src_en.asp"
    }
    p=session.post("http://192.168.1.1/boaform/admin/formRteMacFilter",data=enableLoad)
    print("enabled mac filter")


def switchToMacFilter():
    switchMacLoad={
	"macFilterEnble": "on",
	"excludeMode": "on",
	"action": "chmod",
	"bcdata": "le",
	"submit-url": "http://192.168.1.1/secu_macfilter_src_en.asp"
    }
    p=session.post("http://192.168.1.1/boaform/admin/formRteMacFilter",data=switchMacLoad)
    print("switched to mac filter")

def ApplyTheChange():
    applyChange={
	"macFilterEnble": "on",
	"excludeMode": "on",
	"action": "mode",
	"bcdata": "le",
	"submit-url": "http://192.168.1.1/secu_macfilter_src_en.asp"
    }
    print("applied the settings bam dead")
    p=session.post("http://192.168.1.1/boaform/admin/formRteMacFilter",data=applyChange)


switchPi="<a href = \"/dns?blk=pi\" ><button>Switch Dns to Pi-Hole</button></a>"
switchCloud="<a href = \"/dns?blk=cl\" ><button>Switch Dns to CloudFare</button></a>"

app=flask.Flask(__name__)
app.config['DEBUG'] = True


@app.route('/', methods=['GET'])
def home():
    return "<h1>Welcome to Router Control api -Cp</h1><p>This site is a prototype API for router control using pi.</p> <a href=\"/clientList\"><button>clientList</button></a><br>"+switchPi+switchCloud


# changing DNS
@app.route('/dns',methods=['GET'])
def chaneDns():
    swich=""
    if 'blk' in rq.args:
        if(rq.args['blk']=="pi"):
            print("switch dns to pi")
            swich="block"
            # changeDnsFunc("pi")
        elif(rq.args["blk"]=="cl"):
            print("switch to cloudfare")
            swich="noBlock"
    print("dns change requested")
    if(swich!=""):
        changeDnsFunc(swich)
        return "<h1>Dns Change</h1><p>Dns Changed to "+swich+"</p>"
    else:
        return "<h1>not a valid Dns mentioned</h1>"

# kill Switch
@app.route('/KillSwitchUltimateCyril',methods=['GET'])
def killChangePAss():
    return "<h1>Welcome To the Kill page Router</h1><br><br><a href=\"/KillSwitchUltimateCyril/youveKilledtheGame/c13371925\"><button>Kill Everyones Connection</button></a>"



@app.route('/KillSwitchUltimateCyril/youveKilledtheGame/c13371925',methods=['GET'])
def kill():
    print("killing everyone in 3..2..1")
    switchToEnable()
    switchToMacFilter()
    ApplyTheChange()
    return "<h1>You've disconnected everyone from the network</h1>"


@app.route('/cyril/says/heal/the/router',methods=['GET'])
def heal():
    return "<h1>welcome to the healer</h1> <br><a href = \"/cyril/says/heal/the/router/h/e/a/l/says/the/healer\"><button>healsaysthehealer</button></a>"



@app.route('/cyril/says/heal/the/router/h/e/a/l/says/the/healer',methods=['GET'])
def healer():
    hl={
	"macFilterEnble": "off",
	"excludeMode": "on",
	"action": "sw",
	"bcdata": "le",
	"submit-url": "http://192.168.1.1/secu_macfilter_src_en.asp"
    }
    p=session.post("http://192.168.1.1/boaform/admin/formRteMacFilter",data=hl)
    return "<h1>healed</h1>"
# get client list
@app.route('/clientList',methods=['GET'])
def clientList():
    print("List of Clients")
    a=list_clients()
    return "<h1>client list</h1><p>List of clients</p>"+a


# change the password
@app.route('/passChange', methods=['GET'])
def apid():
    ret="welcome "
    if 'ssid' in rq.args:
        print(rq.args['ssid'])
        ret=ret+ "<h2>reached<h2>"
    if 'pass' in rq.args:
        print(rq.args['pass'])
        ret=ret+ "<h2>got pass<h2>"
    if ('pass' in rq.args )and ('ssid' in rq.args):
        # changePass(ssid=rq.args['ssid'],newPass=rq.args['pass'])
        print("password changed")
        return "<h3> ssid = " + rq.args['ssid']+"<br> password  = "+rq.args['pass']+"</h3>"
    return ret




app.run(host= '0.0.0.0')




