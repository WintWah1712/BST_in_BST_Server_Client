import socket
import sys

class Client:
    def __init__(self):
        self.target_host = 'localhost'
        self.target_port = 9000

    # _______________Receive Data from Server________________
    def runClient(self,data:'register or lgoin'):
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((self.target_host, self.target_port))

        client.send(data)

        recvFromServer = client.recv(4096)

        recvFromServer= recvFromServer.decode('utf-8')
        # print(type(recvFromServer))
        status , message, amount = recvFromServer.split(' ')

        if status == '500':
            print(status, message, amount)
        elif status == '600':
            print(status, message , amount)
        elif status == '400':
            print( status , message , amount)
        elif status == '201':
            print(status,message, amount)
        elif status == '404':
            print(status , message , amount)
        elif status == '200':
            print(status , message , amount)
            while True:
                # ______________________Transcation Options__________________
                print("\n_____Transcation______")
                menu = input("[+]Press => 3 to Deposit\n[+]Press => 4 to Withdraw\n[+]Press => 5 to Transfer\n[+]Press => 6 to Exit ")
                if menu == '3':
                    print('\n________Deposit_________')
                    d_amount = input('Please enter Deposit amount :> ')
                    data = menu + ' ' + message + ' ' + amount + ' ' + d_amount + ' ' + '0'

                elif menu == '4':
                    print('________Withdraw_________')
                    w_amount = input('Please enter Withdraw amount :> ')
                    data = menu + ' ' + message + ' ' + amount + ' ' + w_amount + ' ' + '0'

                elif menu == '5':
                    print('\n________Transfer_________')
                    t_name = input('Please enter Transfer name :> ')
                    t_amount = input('Please enter Transfer amount :> ')
                    data = menu + ' ' + message + ' ' + amount + ' ' + t_amount + ' ' + t_name

                elif menu == '6':
                    sys.exit()


                try:
                    data = bytes(data, 'utf-8')
                    self.runClient(data)
                except Exception as err:
                    print('Register Again !')
                break


        client.close()

# ____________________Client Login and Register Option_______________________
    def option(self):
        option = input("\n[+]Press => 1 to Register\n[+]Press => 2 to Login! ")
        if option=='1':
            r_name = input("Enter username to Register=>: ")
            r_pw = input("Enter password to Register=>: ")
            r_pw2 = input("Enter password again to confirm=>: ")
            if r_pw == r_pw2:
                r_amount = input("Enter your amount=>: ")
                r_allData= option+' '+r_name+' '+r_pw+' '+r_amount+' '+'0'
                r_allData:bytes = bytes(r_allData,'utf-8')
                self.runClient(r_allData)
        elif option =='2':
            l_name = input("Enter username to Login=>:")
            l_pw = input("Enter password to Login=>:")
            l_allData = option+' '+l_name+' '+l_pw+' '+'0'+' '+'0'
            l_allData:bytes = bytes(l_allData,'utf-8')
            self.runClient(l_allData)

if __name__ == "__main__":
    tcpClient:Client=Client()
    while True:
        tcpClient.option()





