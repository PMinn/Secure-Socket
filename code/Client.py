####################################################
#  D1014636 潘子珉                                      									
####################################################
#import sys
import socket
import ssl
import eel
eel.init('gui', allowed_extensions=['.js', '.html'])

PORT = 6666
recv_buff_size = 1024			# Receive buffer size
SERVER_CERT = './Openssl/server.cer'
CLIENT_CERT_PATH = './Openssl/'

'''
def delete(listbox):
   listbox.delete(0,tk.END)
'''

def append(msgType ,txt):
    eel.writeMsg(msgType, txt)

@eel.expose
def main(serverIP, val1):
    CLIENT_CERT = CLIENT_CERT_PATH + 'client.cer'
    CLIENT_KEY = CLIENT_CERT_PATH + 'client.key'
    
	# Verify server Certificate
    ctx = ssl.create_default_context(ssl.Purpose.SERVER_AUTH, cafile=SERVER_CERT)
    ctx.load_cert_chain(certfile=CLIENT_CERT, keyfile=CLIENT_KEY)
    
    consoleFmt = "%-25s %s"
    # Create a TCP client socket
    cSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    append(2, consoleFmt % ("create socket",""))
    
    # Wrap socket
    ssl_conn = ctx.wrap_socket(cSocket, server_side=False, server_hostname=serverIP)
    
    # Connect to server
    print('Connecting to %s port %s' % (serverIP, PORT))
    try:
        ssl_conn.connect((serverIP, PORT))
    except Exception as msg:
        append(-1, consoleFmt % ("socket error", msg))
        return
    append(2, consoleFmt % ("socket connect",""))
#    in1 = input('Input a integer: ')
#    val1 = int(in1)
    val1 = val1 - 1
	# Send message to server
    val1Str = str(val1)
    ssl_conn.send(val1Str.encode('utf-8'))
    append(0, consoleFmt % ("send", f"data: {val1Str}"))
    # Receive server reply, buffer size = BUF_SIZE
    
    server_reply = ssl_conn.recv(recv_buff_size)
    while server_reply:
        server_utf8 = server_reply.decode('utf-8')
        print(server_utf8)
        append(1, consoleFmt % ("recv", f"data: {server_utf8}"))
        server_count = int(server_utf8)
        if server_count >= 0:
            server_count = server_count - 1
            val1Str = str(server_count)
            append(0, consoleFmt % ("send", f"data: {val1Str}"))
            
            ssl_conn.send(val1Str.encode('utf-8'))
            server_reply = ssl_conn.recv(recv_buff_size)
        else:
            break
    append(2, consoleFmt % ("socket close",""))
    ssl_conn.close()
    cSocket.close()

# end of main

eel.start('client.html', size=(500, 500),port=0)  # Start