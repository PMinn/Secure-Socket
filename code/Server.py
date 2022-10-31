####################################################
#  D1014636 潘子珉                                      									
####################################################
import socket
import ssl
import eel
eel.init('gui', allowed_extensions=['.js', '.html'])

PORT = 6666
backlog = 5
recv_buff_size = 1024			# Receive buffer size
SERVER_CERT = './Openssl/server.cer'
SERVER_KEY = './Openssl/server.key'
CLIENT_CERT = './Openssl/client.cer'

'''
def delete(listbox):
    listbox.delete(0,tk.END)
'''

def append(msgType ,txt):
    eel.writeMsg(msgType, txt)

@eel.expose
def main():
    # Create  context & Load Certificate
    ctx = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    ctx.verify_mode = ssl.CERT_REQUIRED
    ctx.load_cert_chain(certfile=SERVER_CERT, keyfile=SERVER_KEY)
    ctx.load_verify_locations(cafile=CLIENT_CERT)
	
	# Create a TCP Server socket
    srvSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    srvSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    srvSocket.bind(('', PORT))
    srvSocket.listen(backlog)
    
    consoleFmt = "%-25s %s"
    # Create a TCP Server socket
    srvSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    append(2, "create socket")
    # Enable reuse address/port
    srvSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    append(2, "setsockopt")
    # Bind 	on any incoming interface with PORT, '' is any interface
    print('Starting up server on port: %s' % (PORT))
    srvSocket.bind(('', PORT))
    append(2, consoleFmt % ("bind", f" port: {PORT}"))
    # Listen incomming connection, connection number = backlog (5)
    srvSocket.listen(backlog)
    append(2, "socket listen")
    
    
    # Accept the incomming connection
    print('Waiting to receive message from client')
    client, (rip, rport) = srvSocket.accept()
    
    ssl_conn = ctx.wrap_socket(client, server_side=True)
    
    # Receive client message, buffer size = BUF_SIZE
    client_msg = ssl_conn.recv(recv_buff_size)
    
    while client_msg:
        client_utf8 = client_msg.decode('utf-8')
        print(client_utf8)
        append(1, consoleFmt % ("recv", f"data: {client_utf8}"))
        client_count = int(client_utf8)
        
        if client_count >= 0:
            # Send message to client
            client_count = client_count - 1
            server_reply = str(client_count)
            append(0, consoleFmt % ("send", f"data: {server_reply}"))
            ssl_conn.send(server_reply.encode('utf-8'))
            client_msg = ssl_conn.recv(recv_buff_size)
        else:
            break

    # Close the TCP socket
    append(2, "socket close")

    ssl_conn.close()
    client.close()
    srvSocket.close()
# end of main

eel.start('server.html', size=(500, 500),port=0)  # Start