from wserver import WebServer

ssid = 'ssid'
password = 'password'

server = WebServer(ssid, password)
server.connect()

f = open('/static/index.html')
html = f.read()
f.close()

pages = {
    "/": "/static/index.html",
    "/page2": "/static/page2.html"
    }

server.start(pages)
