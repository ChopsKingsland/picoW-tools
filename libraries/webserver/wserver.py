import network
import socket
import time

class WebServer:
    """
    Connect to a network and start a web server
    
    :param ssid: The network name
    :type ssid: string
    
    :param password: The network password
    :type password: string
    """
    
    def __init__(self, ssid, password):
        self.ssid = ssid
        self.password = password
        
    def connect(self):
        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)
        wlan.connect(self.ssid, self.password)
        
        max_wait = 10
        while max_wait > 0:
            if wlan.status() < 0 or wlan.status() >= 3:
                break
            max_wait -= 1
            print('waiting for connection...')
            time.sleep(1)

        if wlan.status() != 3:
            raise RuntimeError('network connection failed')
        else:
            print('connected')
            status = wlan.ifconfig()
            print(f'IP: {status[0]}')
    
    def start(self, pagesDict):
        addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]

        s = socket.socket()
        s.bind(addr)
        s.listen(1)

        print(f'Listening on {addr}')
        
        while True:
            try:
                cl, addr = s.accept()
                print(f'Client connected from {addr}')
                request = cl.recv(1024)
                #print(request)
                
                request = str(request)
                try:
                    path = request.split('GET ')[1].split(' HTTP')[0]
                    
                    print(f'looking for page {path}')
                    
                    if path in pagesDict:
                        page = pagesDict[path]
                    else:
                        page = "/static/index.html"
                        
                    f = open(page)
                    response = f.read()
                    f.close()
                    
                    cl.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
                    cl.send(response)
                    cl.close()
                except:
                    response = "an error has occurred"
                    
                    cl.send('HTTP/1.0 200 OK\r\nContent-type: text/plain\r\n\r\n')
                    cl.send(response)
                    cl.close()
                
            except OSError as e:
                cl.close()
                print('connection closed')
