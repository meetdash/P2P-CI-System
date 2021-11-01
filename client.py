'''
When a peer wishes to join the system, it
1. instantiates an upload server process listening to any available local port.
2. creates a connection to the server at the well-known port 7734 and passes information about itself and its RFCs to the server.
3. keeps this connection open until it leaves the system.
4. may send requests to the server over this open connection and receive responses (e.g., the hostname and upload port of a server containing a particular RFC).
5. when it wishes to download an RFC, it opens a connection to a remote peer at 
the specified upload port, requests the RFC, receives the file and stores it locally, and the closes this download connection to the peer.
'''

from socket import *

HOST = 'localhost'
PORT = 7734

def register():
	csock = socket(AF_INET, SOCK_STREAM)
	print("Connecting to server %s on port %s" % (HOST, PORT))
	return csock.connect((HOST, PORT))

def publish(csock, rfc_list):
		msg = 'Hosted RFC details: ' + str(rfc_list) + '\n'
		fragments = []

		try:
			csock.sendall(msg.encode())
			while True: 
			    chunk = csock.recv(1024) # however large we want
			    fragments.append(chunk.decode())
			    print(fragments)
			    if '\n' in chunk.decode():
			    	break
		except error as e:
			print("Socket error: ", e)
		except Exception as e:
			print("Other exception: ", e)

		server_response = ''.join(fragments)
		if 'Success' in server_response:
			print("Published: ", server_response)
			return 1
		return 0

def search_rfc(csock, rfc):
	msg = 'Requesting details for RFC: ' + str(rfc) + '\n'
	fragments = []

	try:
		csock.sendall(msg.encode())
		while True:
		    chunk = csock.recv(1024) # however large we want
		    fragments.append(chunk.decode())
		    print(fragments)
		    if '\n' in chunk.decode():
		    	break
	except error as e:
		print("Socket error: ", e)
	except Exception as e:
		print("Other exception: ", e)

	server_response = ''.join(fragments)
	if 'Found' in server_response:
		return server_response # extract client addr + port and return
	else:
		return (0, 0)

def login():
	pass

def logout():
	pass

def peer_connect():
	pass

if __name__ == '__main__':
	# parser = argparse.ArgumentParser(description='Socket Server')
	# parser.add_argument('--port', action='store', dest='port', type=int, required=True)
	# given_args = parser.parse_args()
	csock, serv_addr = register(rfcs)
	rfcs = [{'RFC #': 1234, 'RFC Title': 'Sample RFC 1', 'Port': 7890}, {'RFC #': 1212, 'RFC Title': 'Sample RFC 2', 'Port': 8989}]
	
	if not publish(csock, rfcs):
		print("Unable to publish RFCs on server")
		exit()

	peer_addr, peer_port = search_rfc('Sample RFC 2')
	if peer_port == 0:
		print("RFC not hosted at any peer.")
		exit()

	