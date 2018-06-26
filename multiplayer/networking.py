import socket

class communicate:
    def __init__(self,ip_address,name,port):
        self.name = name
        self.serverSocket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        self.serverSocket.bind(('',port))
        self.player2name = ''
        self.is_connected = False
        self.ip_address = ip_address
    
    def send_data(self,data):
        self.serverSocket.sendto(bytes(data,'utf-8'),self.ip_address)
        return True

    def get_data(self):
        if self.is_connected:
            data, address = self.serverSocket.recvfrom(1024)
            data = data.decode('utf-8')
            if(data=="terminate"):
                print("received terminate signal")
                self.closeconnection()
            
            assert (address==self.ip_address)

            return data
        else :
            print("connection term in get_data")
            return False

    def wait_connection(self):
        self.player2name, self.address = self.serverSocket.recvfrom(1024)
        self.player2name = self.player2name.decode('utf-8')
        print(self.address)
        assert self.address == self.ip_address

        if not str(self.player2name)=="terminate":

            print("connected successfully to "+str(self.player2name)+" from "+str(self.address))
            self.serverSocket.sendto(bytes(self.name,'utf-8'),self.address)
            self.is_connected = True
            return True

        else:
            print("received term signal from ip: "+str(self.address))
            self.closeconnection()
            self.is_connected=False
            return False
    
    def createConnection(self):
        print("creating connection...")
        self.serverSocket.sendto(bytes(self.name,'utf-8'),self.ip_address)
        try:
            self.player2name, self.address = self.serverSocket.recvfrom(1024)
            self.player2name = self.player2name.decode('utf-8')

            print("got connected to: "+str(self.player2name))
            self.is_connected=True
        
        except Exception as e:
            print (e)
            print("connection timed out!")
            self.closeconnection()

    def closeconnection(self):
        if(self.is_connected):
            self.serverSocket.sendto(bytes("terminate",'utf-8'),self.address)
        try:
            self.serverSocket.close()
        except:
            print("socket already closed!")
        self.is_connected = False
        print("connection Terminated")

    def get_connection_status(self):
        if(self.is_connected):
            return (self.name,self.address)
        else :
            return False
