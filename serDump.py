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



app=flask.Flask(__name__)
app.config['DEBUG'] = True
@app.route('/', methods=['GET'])
def home():
    return "<h1>Distant Reading Archive</h1><p>This site is a prototype API for distant reading of science fiction novels.</p>"

@app.route('/dns',methods=['GET'])
def chaneDns():
    swich=""
    if 'blk' in rq.args:
        if(rq.args['blk']=="pi"):
            print("switch dns to pi")
            swich="pi"
        elif(rq.args["blk"]=="cl"):
            print("switch to cloudfare")
            swich="cldfare"
    print("dns change requested")
    return "<h1>Dns Change</h1><p>Dns Changed to "+swich+"</p>"



# get client list
@app.route('/clientList',methods=['GET'])
def clientList():
    print("List of Clients")
    a=list_clients()
    return "<h1>client list</h1><p>List of clients</p>"+a


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




app.run()




