from socket import *
class Server:

    def __init__(self): # Constructor -> Creates connection and sock, conn variables to be used
        self.sock = socket(AF_INET, SOCK_STREAM)
        self.Host = '127.0.0.1'
        self.Port = 12000
        self.sock.bind((self.Host, self.Port))
        self.sock.listen()
        self.conn, self.addr = self.sock.accept()
        print("Connected to: ",  self.addr)
        self.conn.sendall(("Connection established at Port: " + str(self.Port)).encode("utf-8"))

    def receiveMessage(self): #Gets messages from client, executes methods based on commands
        while True: #Keeps the good times rolling
         data = self.conn.recv(1024).decode("utf-8") #receives message
         self.conn.sendall(data.encode("utf-8")) #tells client what message it received
         if data[0:3].upper() == 'GET': #Execute methods depending on command
             self.Get(data)
         if data[0:3].upper() == "PUT":
             self.Put(data)
         if (data[0:5].upper() == "CLOSE"):
             self.Close()
         if data == "QUIT": #QUIT the server loop will exit conn.close and sock.close run
             break
        self.conn.close()
        self.sock.close()

    def Get(self, data):
     try: # Try catch for errors
        filename = data[4:] #Reads file name from message
        filename = filename.strip() #removes spaces
        f = open("C:/Users/bkeel/PycharmProjects/SocketProgramming/ServerFiles/" + filename, "rb") #Open file stream reads bytes
        self.conn.sendfile(f) #send the file stream/ read bytes
        f.close() # close da stream
        self.conn.sendall(("Sent: " + filename).encode("utf-8")) # confirmation message

     except:
        print("File sent unsuccesfully. ") # run into error display message
        self.conn.send("ERROR".encode("utf-8")) #Sends error so that the client doesn't wait to receive nothing.

    def Put(self, data):
        try:
         filename = self.conn.recv(1024).decode("utf-8") #Receives filename from client
         if(filename!="ERROR"): # Error checks client side, dont write if client has issues
          f = open("C:/Users/bkeel/PycharmProjects/SocketProgramming/ServerFiles/" + filename, "wb") # open stream for writing server directory
          dat = self.conn.recv(1024) # receive file to be writen
          f.write(dat) # write da file
          f.close() # close da stream
          print(filename + " Put") # confirmation message
          self.conn.sendall("Server: File received.".encode("utf-8")) #send confirmation message to client
         else: 1/0 #throw error
        except:
            print("File put unsuccesfully")

    def Close(self):
        try:
            self.sock.close()  #Connection with client now closed, listen for new client
            print("Connection Closed")
            self.sock = socket(AF_INET, SOCK_STREAM)
            self.sock.bind((self.Host, self.Port))
            print("Ready to receive... ")
            self.sock.listen()
            self.conn, self.addr = self.sock.accept()
        except:
           print("ERROR")
















