import socket
import sys
import threading


def SocketSaida(s): #diretrizes para a thread
    global byeFlag
    print("Digite 'sair' para encerrar o chat")
    while True:
        if byeFlag:
            try:
                str = s.recv(100).decode()
                print("\r>>> " + str + "\n<<<", end="", flush=True)
            except:
                print("Conexão encerrada")
                break

            if str == "sair":
                byeFlag = 0;
                break
        
    print("Usuario remoto desconectado!!!")
    s.close()
    sys.exit()
    
def SocketEscrita(s): #diretrizes para a thread
    global byeFlag
    while True:
        if byeFlag:
            str = input("<<< ") #envio da msg
            s.send(str.encode())
            if str == "sair":
                print("Sinal para terminar o chat, enviado!!!")
                byeFlag = 0;
                s.close()
                sys.exit()
        



s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #cria socket e pergunta o que fazer
byeFlag = 1;
ch = input("Para conectar ao parceiro digite [1] ou [2] para aguardar a conexão de entrada. Digite sua escolha:")

if ch == "1": #caso escolha for 1
    host = input("Digite o IP do parceiro :") #IP do parceiro que quer ser conectar
    port = 54321 #porta utilizada
    s.connect((host, port))
    threading.Thread(target=SocketSaida, args=(s,)).start() #inicio de thread
    threading.Thread(target=SocketEscrita, args=(s,)).start() #inicio de thread
    
elif ch == "2": #caso a escolha seja 2
    host = ''
    port = 54321 #porta tem que ser igual a da escolha 1
    s.bind((host, port))
    s.listen(2)              # Aguarda conexão com o parceiro.
    print("Aguardando conexão...")
    while True:
        c, addr = s.accept()     # Conexão estabelecida com o parceiro.
        threading.Thread(target=SocketSaida, args=(c,)).start() #inicio de thread
        threading.Thread(target=SocketEscrita, args=(c,)).start()#inicio de thread

else:
    print("Opção incorreta")
    sys.exit()
