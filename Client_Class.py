from socket import *
class Client:

    def __init__(self): # Constructor, defines varibles, functions as the initial OPEN command
        self.Host = '127.0.0.1'
        while (True): #Just checking formatting
            s = input("Open a connection using OPEN#PortNumber")
            if (s[0:5] == "OPEN#"):
                break
            print("Incorrect Input. Type Open# followed directly by the desired port number")
        try:
         self.Port = int(s[s.index("#") + 1:]) #Reads port number from messg
         self.sock = socket(AF_INET, SOCK_STREAM) # initilizes sock
         self.sock.connect((self.Host, self.Port)) #Connects
         print(self.sock.recv(1024).decode("utf-8")) #Confirmation message
        except:
           print("ERROR. Try again")
           self.__init__() #error in input try again


    def SendMessage(self): #Allows user to send to server, commands, messages...
        while True:
            s = input("Message. ")
            self.sock.sendall(s.encode("utf-8"))
            data = self.sock.recv(1024).decode("utf-8")
            print("Received", data)
            if s[0:3].upper() == 'GET':  #Methods based on message commands
                self.Get(s)

            if (data[0:5].upper() == "OPEN#"):
                print("Connection already established. Close connection first.")
            if data[0:3].upper() == "PUT":
                self.Put(s)

            if (data[0:5].upper() == "CLOSE"):
                data = self.Close(s)


            if data == "QUIT":
                break


    def Get(self,s):
        try:
            filename = s[4:] #Gets filename from message
            filename = filename.strip() # remove white space
            dat = self.sock.recv(1024) #Gets error message or file from server
            if(dat.decode("utf-8")!="ERROR"): #Checks if server had an error
             f = open("C:/Users/bkeel/PycharmProjects/SocketProgramming/ClientFiles/" + filename, "wb") #Open file stream to  write to directory change for your machine
             f.write(dat) # write da file
             f.close() # close da stream
             str = self.sock.recv(1024).decode("utf-8") #confirmation message
             print(str)
            else:
                print("Server error")
                1/0 #throws an error so except message displayed

        except:
           print("File not Gotten")
    def Put(self,s):
        try:
         filename = s[4:]
         filename = filename.strip()
         f = open("C:/Users/bkeel/PycharmProjects/SocketProgramming/ClientFiles/" + filename, "rb") #Open file stream to read file
         self.sock.send(filename.encode("utf-8")) #send the filename so server knows what filename to write
         self.sock.sendfile(f) #send the file
         f.close() # close da stream
         t = self.sock.recv(1024).decode("utf-8") # Confirmation message
         print(t) # confirmation message
        except:
            self.sock.send("ERROR".encode("utf-8")) #lets server know there is an error on client side
            print("Unable to put file. ")
    def Close(self,s):
        try:
            self.sock.close() #close the sock
            print("Connection Closed")
            ans = input("Would you like to connect to a diff server? (Y/N) ") #If yes go through open process, else quit
            if (ans.upper() == "Y"):
             self.sock = socket(AF_INET, SOCK_STREAM)
             self.Port = int(input("Enter new Port #: ")) # change port number to one user requests
             self.sock.connect((self.Host, self.Port))
             return s
            else:
             return "QUIT"
        except:
            print("ERROR")






