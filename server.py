import socket
class Node:
    def __init__(self,data):
        self.CharAlphbet=data
        self.c_right=None
        self.c_left=None

# ________________Char BST__________________
def dataInsertion():
    root = Node('p')

    root.c_left = Node('h')
    root.c_left.c_left = Node('d')
    root.c_left.c_right = Node('l')
    root.c_left.c_left.c_left = Node('b')
    root.c_left.c_left.c_right = Node('f')
    root.c_left.c_right.c_left = Node('j')
    root.c_left.c_right.c_right = Node('n')
    root.c_left.c_left.c_left.c_left = Node('a')
    root.c_left.c_left.c_left.c_right = Node('c')
    root.c_left.c_left.c_right.c_left = Node('e')
    root.c_left.c_left.c_right.c_right = Node('g')

    root.c_left.c_right.c_left.c_left = Node('i')
    root.c_left.c_right.c_left.c_right = Node('k')
    root.c_left.c_right.c_right.c_left = Node('m')
    root.c_left.c_right.c_right.c_right = Node('o')

    root.c_right = Node('t')
    root.c_right.c_left = Node('r')
    root.c_right.c_right = Node('x')
    root.c_right.c_left.c_left = Node('q')
    root.c_right.c_left.c_right = Node('s')
    root.c_right.c_right.c_left = Node('v')
    root.c_right.c_right.c_right = Node('y')
    root.c_right.c_right.c_left.c_left = Node('u')
    root.c_right.c_right.c_left.c_right = Node('w')
    root.c_right.c_right.c_right.c_right = Node('z')
    return root

# __________________Root Length BST__________________
class LenghtBST:
    def __init__(self,data):
        self.data=data
        self.info=[]
        self.infoPw=[]
        self.infoAmount=[]
        self.left=None
        self.right=None

def RootLengthTree():
    root=None
    list_length=[16,8,24,4,12,20,28,2,6,10,14,18,22,26,29,1,3,5,7,9,11,13,15,17,19,21,23,25,27,30]
    length=len(list_length)
    print(length)

    for i in range(0,length):
        print("data",list_length[i])
        root = insert(root,list_length[i])
    return root

def insert(node, key):

    # Return a new node if the tree is empty
    if node is None:
        return LenghtBST(key)
    # Traverse to the right place and insert the node
    if key < node.data:
        node.left = insert(node.left, key)
    else:
        node.right = insert(node.right, key)

    return node

# _________________TCP Server______________________
class TCPserver:
    def __init__(self):
        self.server_ip='localhost'
        self.server_port = 9000
        self.sock = None
        self.AlphaRoot = dataInsertion()
        self.RLTroot = RootLengthTree()
        if self.AlphaRoot:
            print('AlphaDatabase created!')
            self.inorderForAlpha(self.AlphaRoot)
            print('\n')
        if self.RLTroot:
            print('[+][+] Root lenght tree created')
            self.inorderForRLT(self.RLTroot)
            print('\n')

    def inorderForRLT(self,RLTroot):
        if RLTroot is not None:
            self.inorderForRLT(RLTroot.left)
            print(RLTroot.data,' >',end=' ')
            self.inorderForRLT(RLTroot.right)

    def inorderForAlpha(self,AlphaRoot):
        if AlphaRoot is not None:
            self.inorderForAlpha(AlphaRoot.c_left)
            print(AlphaRoot.CharAlphbet,' >',end=' ')
            self.inorderForAlpha(AlphaRoot.c_right)


    def main(self):
        server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        server.bind((self.server_ip, self.server_port))
        server.listen(1)
        print(f'[*] Listening on {self.server_ip}:{self.server_port} >:')
        while True:
            client, address = server.accept()
            print(f'[*] Accepted connection from {address[0]}:{address[1]}')
            self.handle_client(client)

# __________________Receive and Send Data to CLient____________________
    def handle_client(self,client):
        with client as self.sock:
            request = self.sock.recv(4096)
            client_sms=request.decode("utf-8")
            print(f'[*] Received:',client_sms)
            option, c_uname , c_pw, c_amount,t_name=client_sms.split(' ')
            if option=='1':
                print("This is for registration")
                success =self.forRegistration(c_uname,c_pw,c_amount)
                if success == 'fail':
                    data = '400'+' '+'Data_Already_Exit'+' '+c_uname
                    data = bytes(data,'utf-8')
                    self.sock.send(data)
                elif success == 'success':
                    data = '201'+' '+'SuccessRegistration'+' '+c_uname
                    data = bytes(data,'utf-8')
                    self.sock.send(data)

            elif option == '2':
                self.loginAlpha(c_uname,c_pw)

            elif option == '3':
                print('***\nDeposit Transcation***')
                self.forDeposit(c_uname,c_pw,c_amount,option)

            elif option == '4':
                print('***\nWithdraw Transcation***')
                self.forWithdraw(c_uname,c_pw,c_amount,option)

            elif option == '5':
                print('***\nTransfer Transcation***')
                self.forTransfer(c_uname,c_pw,c_amount,option,t_name)

# __________________Check Data from RLT_______________________
    def RLT_checking(self,RLTroot,name,Length):
        if RLTroot is None:
            print('RLT root is empty cannot be proceed! in Login!')
        if RLTroot.data == Length:
            print('from RLT_checking_searchinRLT:', RLTroot.data)
            return RLTroot.info , RLTroot.infoAmount
        elif RLTroot.data < Length :
            return self.RLT_checking(RLTroot.right, name,Length)
        elif RLTroot.data > Length:
            return self.RLT_checking(RLTroot.left, name,Length )

# _____________________For Deposit Transcation_______________________
    def forDeposit(self,lname,l_amount,d_amount,option):
            name_length = len(lname)
            rlt_nameinfo,rlt_amount = self.RLT_checking(self.RLTroot,lname,name_length)
            length = len(rlt_nameinfo)

            for i in range(0,length):
                if lname == rlt_nameinfo[i]:
                    l_amount = int(l_amount)
                    typeAmount = type(l_amount)
                    print('Login amount {0} {1}'.format(l_amount,typeAmount))
                    result = l_amount+int(d_amount)
                    typeResult = type(result)
                    print('Deposit amount result {0} {1}'.format(result, typeResult))
                    update_userinfo = self.forUpdateUserInfo(self.RLTroot,lname,name_length,result,option)
                    print('Deposit function : ',update_userinfo)
                    data = '200'+' '+lname+' '+update_userinfo
                    data = bytes(data,'utf-8')
                    self.sock.send(data)

# _____________________For Withdraw Transcation_______________________
    def forWithdraw(self,lname,l_amount,w_amount,option):
            name_length = len(lname)
            rlt_nameinfo,rlt_amount = self.RLT_checking(self.RLTroot,lname,name_length)
            length = len(rlt_nameinfo)

            for i in range(0,length):
                if lname == rlt_nameinfo[i]:
                    l_amount = int(l_amount)
                    typeAmount = type(l_amount)
                    print('Login amount {0} {1}'.format(l_amount,typeAmount))
                    w_amount = int(w_amount)
                    if (w_amount <= l_amount):
                        result = l_amount-w_amount
                        typeResult = type(result)
                        print('Withdraw amount result {0} {1}'.format(result, typeResult))
                        update_userinfo = self.forUpdateUserInfo(self.RLTroot,lname,name_length,result,option)
                        print('Withdraw function : ',update_userinfo)
                        data = '200'+' '+lname+' '+update_userinfo
                        data = bytes(data,'utf-8')
                        self.sock.send(data)
                    else:
                        print('Insufficient Balance!')
                        data = '600'+' '+'Insufficient_Balance'+' '+ str(l_amount)
                        data = bytes(data,'utf-8')
                        self.sock.send(data)

# __________________________For Transfer Transcation__________________________
    def forTransfer(self,lname,l_amount,t_amount,option,t_name):
            name_length = len(lname)
            t_name_length = len(t_name)
            rlt_nameLoginInfo,rlt_loginAmount = self.RLT_checking(self.RLTroot,lname,name_length)
            print('RLT Login Data {0} {1}'.format(rlt_nameLoginInfo,rlt_loginAmount))
            rlt_nameTransferInfo,rlt_transferAmount = self.RLT_checking(self.RLTroot,t_name,t_name_length)
            print('RLT Login Data {0} {1}'.format(rlt_nameLoginInfo, rlt_loginAmount))
            length_rltLogin = len(rlt_nameLoginInfo)
            length_rltTransfer = len(rlt_nameTransferInfo)
            for i in range(0,length_rltLogin):
                if lname == rlt_nameLoginInfo[i]:
                    l_amount = int(l_amount)
                    typeAmount = type(l_amount)
                    print('Login amount {0} {1}'.format(l_amount,typeAmount))
                    t_amount = int(t_amount)
                    if l_amount >= t_amount:
                        result = l_amount-t_amount
                        typeResult = type(result)
                        print('Transfer amount result {0} {1}'.format(result, typeResult))
                        update_userinfo = None
                        update_userinfo = self.forUpdateUserInfo(self.RLTroot,lname,name_length,result,option)
                        print('Login User : ',update_userinfo)

                    else:
                        print('Insufficient Balance!')
                        data = '600'+' '+'Insufficient_Balance'+' '+ str(l_amount)
                        data = bytes(data,'utf-8')
                        self.sock.send(data)
            for i in range(0, length_rltTransfer):
                    if t_name == rlt_nameTransferInfo[i]:
                        user_amount = rlt_transferAmount[i]
                        t_amount = int(t_amount)
                        typeAmount = type(t_amount)
                        print('Transfer amount {0} {1}'.format(t_amount,typeAmount))
                        user_amount = int(user_amount)
                        result = user_amount + t_amount
                        typeResult = type(result)
                        print('Transfer amount result {0} {1}'.format(result, typeResult))
                        update_userTransferInfo = None
                        update_userTransferInfo = self.forUpdateUserInfo(self.RLTroot,t_name,t_name_length,result,option)
                        print("Success Transfer {0} ,{1}".format(t_name,update_userTransferInfo))
            data = '200' + ' ' + lname + ' ' + update_userinfo
            data = bytes(data, 'utf-8')
            self.sock.send(data)


# __________________________Update User Information In RLT_________________
    def forUpdateUserInfo(self,RLTroot,name ,Length , result,option):
        if RLTroot is None:
            print('RLT root is empty cannot be proceed! in Login!')
        if RLTroot.data == Length:
            print('from Update_searchinRLT:', RLTroot.data)
            InfoNameLength = len(RLTroot.info)
            print('Name Length : ',InfoNameLength)
            update_amount = None
            update_name = None
            update_pw = None
            for i in range(0, InfoNameLength):
                if RLTroot.info[i] == name:
                    if option == '3' or option == '4':
                        RLTroot.infoAmount[i] = str(result)
                        update_amount = RLTroot.infoAmount[i]
                        print('Type of Result Amount : ', update_amount)
                        return update_amount
                    elif option == '5':
                        RLTroot.infoAmount[i] = str(result)
                        update_amount = RLTroot.infoAmount[i]
                        return update_amount
        elif RLTroot.data < Length :
            return self.forUpdateUserInfo(RLTroot.right, name,Length,result,option)
        elif RLTroot.data > Length:
            return self.forUpdateUserInfo(RLTroot.left, name,Length ,result,option)

# _______________For Register_____________________
    def forRegistration(self,uname , pw ,amount):
        uname  = uname.lower()
        firstData =uname[0]
        Length =len(uname)
        success =self.searchInAlpha(self.AlphaRoot, uname, firstData,Length,pw,amount)
        print('for registartion function : \n',success)
        return success

    def searchInAlpha(self,AlphaRoot, uname , firstData , Lenght , pw,amount ):
        success = None
        alphaNo =ord(AlphaRoot.CharAlphbet)
        firstNo = ord(firstData)
        if AlphaRoot is None:
            print('Alpha root is empty cannot be proceed!')
        if AlphaRoot.CharAlphbet == firstData:
            print("Alpha was found : ",AlphaRoot.CharAlphbet)
            success =self.insertInRLT(self.RLTroot,Lenght,uname,pw,amount)
            print('Return from insertInRLT: \n',success)
            success = success
            return success
        elif alphaNo < firstNo :
            return self.searchInAlpha(AlphaRoot.c_right , uname , firstData , Lenght ,pw ,amount)
        elif alphaNo > firstNo:
            return self.searchInAlpha(AlphaRoot.c_left, uname, firstData, Lenght, pw,amount)

    def insertInRLT(self,RLTroot , Lenght , uname , pw ,amount):
        flag = None
        if RLTroot is None:
            print('RLT root is empty cannot be proceed!')
        if RLTroot.data == Lenght:
            print('for insertInRLT ',RLTroot.data)
            infoLength = len(RLTroot.info)
            print("Info length :",infoLength)
            if infoLength == 0:
                RLTroot.info.append(uname)
                RLTroot.infoPw.append(pw)
                RLTroot.infoAmount.append(amount)
                print(RLTroot.info)
                print(RLTroot.infoPw)
                print(RLTroot.infoAmount)

                flag = 'success'
                print(flag)
                return flag
            else:
                for i in RLTroot.info:
                    if i == uname:
                        print("Already Exit!")
                        flag = 'fail'
                        print(flag)
                        return flag
                RLTroot.info.append(uname)
                RLTroot.infoPw.append(pw)
                RLTroot.infoAmount.append(amount)
                print("Registration Success : ", uname , pw)
                flag = 'success'
                print(flag)
                return flag
        elif RLTroot.data < Lenght :
            return self.insertInRLT(RLTroot.right, Lenght , uname ,pw ,amount)
        elif RLTroot.data > Lenght:
            return self.insertInRLT(RLTroot.left, Lenght , uname ,pw ,amount)

# ____________________For Login____________________________
    def loginAlpha(self,uname , pw ):
        uname  = uname.lower()
        firstData =uname[0]
        Length = len(uname)
        self.login_SearchInAlpha(self.AlphaRoot , uname , firstData , Length ,pw )

    def login_SearchInAlpha(self,AlphaRoot , uname , firstData , Lenght , pw):
        alphaNo = ord(AlphaRoot.CharAlphbet)
        firstNo = ord(firstData)
        if AlphaRoot is None:
            print('Alpha root is empty cannot be proceed!in Login!')
        if AlphaRoot.CharAlphbet == firstData:
            print("Alpha was found : ", AlphaRoot.CharAlphbet)
            self.login_serachinRLT(self.RLTroot, Lenght, uname, pw)

        elif alphaNo < firstNo:
            return self.login_SearchInAlpha(AlphaRoot.c_right, uname, firstData, Lenght, pw)
        elif alphaNo > firstNo:
            return self.login_SearchInAlpha(AlphaRoot.c_left, uname, firstData, Lenght, pw)

    def login_serachinRLT(self,RLTroot , Length , uname , pw ):
        if RLTroot is None:
            print('RLT root is empty cannot be proceed! in Login!')
        if RLTroot.data == Length:
            print('from Login_searchinRLT:',RLTroot.data )
            InfoNameLength = len(RLTroot.info)
            for i in range(0,InfoNameLength):
                if RLTroot.info[i] == uname and RLTroot.infoPw[i]==pw :
                    print("Login Success for User : ",RLTroot.info[i])
                    data ='200'+' '+RLTroot.info[i]+' '+RLTroot.infoAmount[i]
                    data = bytes(data,'utf-8')
                    self.sock.send(data)
            data = '404' +' ' +'Login_Failed!' +' '+'0'
            data = bytes(data,'utf-8')
            self.sock.send(data)

        elif RLTroot.data < Length :
            return self.login_serachinRLT(RLTroot.right, Length , uname ,pw )
        elif RLTroot.data > Length:
            return self.login_serachinRLT(RLTroot.left, Length , uname ,pw )

if __name__ == "__main__":
    tcpServer :TCPserver =TCPserver()
    tcpServer.main()