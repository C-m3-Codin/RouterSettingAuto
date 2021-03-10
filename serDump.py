import flask
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




app=flask.Flask(__name__)
app.config['DEBUG'] = True
@app.route('/', methods=['GET'])
def home():
    return "<h1>Distant Reading Archive</h1><p>This site is a prototype API for distant reading of science fiction novels.</p>"

@app.route('/dns/Block',methods=['GET'])
def chaneDns():
    print("dns changed pi")
    return "<h1>Dns Change</h1><p>Dns Changed to Pi</p>"

@app.route('/dns/NoBlock',methods=['GET'])
def changeDns():
    print("dns changed to Cloudfare")
    return "<h1>Dns Change</h1><p>Dns Changed to cloudFare</p>"

@app.route('/clientList',methods=['GET'])
def clientList():
    print("List of Clients")
    a=list_clients()
    return "<h1>client list</h1><p>List of clients</p>"+a
app.run()




